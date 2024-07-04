import pandas as pd
import unicodedata
import streamlit as st
from io import BytesIO

# Função para remover acentos
def remover_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

# Função para gerar e-mail único
def gerar_email(partes, emails_gerados, dominio):
    excluidas = ['de', 'dos', 'da', 'do', 'com']
    partes_email = [remover_acentos(parte).lower() for parte in partes if parte.lower() not in excluidas and parte.isalpha()]
    email = f"{partes_email[0]}.{partes_email[-1]}@{dominio}"
    if email not in emails_gerados:
        emails_gerados.add(email)
        return email
    for parte in partes_email[1:-1]:
        email_intermediario = f"{partes_email[0]}.{parte}@{dominio}"
        if email_intermediario not in emails_gerados:
            emails_gerados.add(email_intermediario)
            return email_intermediario
    sufixo = 1
    email_base = f"{partes_email[0]}.{partes_email[-1]}"
    while f"{email_base}{sufixo}@{dominio}" in emails_gerados:
        sufixo += 1
    email_final = f"{email_base}{sufixo}@{dominio}"
    emails_gerados.add(email_final)
    return email_final

# Função para verificar e criar e-mails e definir caminhos organizacionais
def verificar_e_criar_email(nome, tipo, df_base, emails_gerados, dominios, org_paths):
    nome_formatado = remover_acentos(nome).title()
    nome_sem_acentos = nome_formatado.lower()
    nome_comparacao = df_base['Nome Completo'].apply(lambda x: remover_acentos(x).lower())
    
    if nome_sem_acentos in nome_comparacao.values:
        usuario_existente = df_base[nome_comparacao == nome_sem_acentos].iloc[0].to_dict()
        usuario_existente['Org Unit Path [Required]'] = org_paths[tipo]
        return usuario_existente
    else:
        partes = nome_formatado.split()
        email = gerar_email(partes, emails_gerados, dominios[tipo])
        emails_gerados.add(email)
        novo_usuario = {
            'Nome Completo': nome_formatado,
            'Email Address [Required]': email,
            'First Name [Required]': partes[0],
            'Last Name [Required]': ' '.join(partes[1:]),
            'Org Unit Path [Required]': org_paths[tipo],
        }
        return novo_usuario

# Função para converter DataFrame para Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
    output.seek(0)
    return output.getvalue()

# Função principal do Streamlit
def main():
    st.title('Criação de E-mails Institucionais')

    uploaded_file_base = st.file_uploader("Carregar arquivo base (base.xlsx):", type='xlsx')
    uploaded_file_teste = st.file_uploader("Carregar arquivo de teste (teste.xlsx):", type='xlsx')

    col1, col2 = st.columns(2)

    with col1:
        dominio_padrao = st.text_input("Domínio Padrão", value='dominio.exemplo.com')
        prefixo_professor = st.text_input("Prefixo para Professores", value='docente')
        prefixo_aluno = st.text_input("Prefixo para Alunos", value='aluno')

    with col2:
        org_padrao = st.text_input("Caminho Organizacional Padrão", value='/Servidores')
        org_professor = st.text_input("Caminho Organizacional para Professores", value='/Servidores')
        org_alunos = st.text_input("Caminho Organizacional para Alunos", value='/Alunos')

    dominios = {
        None: dominio_padrao,
        'PROFESSOR': prefixo_professor + '.' + dominio_padrao,
        'ALUNO': prefixo_aluno + '.' + dominio_padrao,
    }

    org_paths = {
        None: org_padrao,
        'PROFESSOR': org_professor,
        'ALUNO': org_alunos,
    }

    if st.button('Processar Dados'):
        if uploaded_file_base is not None and uploaded_file_teste is not None:
            df_base = pd.read_excel(uploaded_file_base)
            df_teste = pd.read_excel(uploaded_file_teste)

            df_base['Nome Completo'] = df_base['First Name [Required]'] + ' ' + df_base['Last Name [Required]']
            df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(lambda x: 'DESATIVADO' if x == 'Never logged in' else 'ATIVADO')
            df_base = df_base[['Nome Completo', 'Email Address [Required]', 'Status', 'Org Unit Path [Required]']]

            emails_gerados = set(df_base['Email Address [Required]'].tolist())
            resultados = []

            for _, row in df_teste.iterrows():
                tipo_usuario = str(row['Tipo']).strip().upper() if 'Tipo' in df_teste.columns and not pd.isna(row['Tipo']) else None
                resultado = verificar_e_criar_email(row['Nome'], tipo_usuario, df_base, emails_gerados, dominios, org_paths)
                resultados.append(resultado)

            df_resultado_final = pd.DataFrame(resultados)

            if not df_resultado_final.empty:
                excel_data = convert_df_to_excel(df_resultado_final)
                st.success("Dados processados com sucesso.")
                st.download_button(label="📥 Download Excel",
                                   data=excel_data,
                                   file_name="resultados_emails.xlsx",
                                   mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                st.error("DataFrame resultante está vazio, não há dados para exportar.")
        else:
            st.error("Por favor, carregue ambos os arquivos antes de processar.")

if __name__ == "__main__":
    main()
