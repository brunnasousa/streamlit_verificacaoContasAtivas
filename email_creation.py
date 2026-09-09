import pandas as pd
import unicodedata
import streamlit as st
from io import BytesIO


# Função para remover acentos
def remover_acentos(texto):
    if pd.isna(texto):
        return ""
    return unicodedata.normalize('NFKD', str(texto)).encode('ascii', 'ignore').decode('ascii')


# Função para gerar e-mail único
def gerar_email(partes, emails_gerados, dominio):
    excluidas = ['de', 'dos', 'da', 'do', 'das', 'e', 'com']

    partes_email = [
        remover_acentos(parte).lower().strip()
        for parte in partes
        if str(parte).strip()
        and remover_acentos(parte).lower().strip() not in excluidas
        and remover_acentos(parte).replace(" ", "").isalpha()
    ]

    # Se não sobrar nenhuma parte válida
    if not partes_email:
        return None

    # Se só tiver uma parte, usa só ela
    if len(partes_email) == 1:
        email = f"{partes_email[0]}@{dominio}"
        if email not in emails_gerados:
            emails_gerados.add(email)
            return email

        sufixo = 1
        while f"{partes_email[0]}{sufixo}@{dominio}" in emails_gerados:
            sufixo += 1

        email_final = f"{partes_email[0]}{sufixo}@{dominio}"
        emails_gerados.add(email_final)
        return email_final

    # Caso normal: primeiro.ultimo
    email = f"{partes_email[0]}.{partes_email[-1]}@{dominio}"
    if email not in emails_gerados:
        emails_gerados.add(email)
        return email

    # Tenta primeiro.nome_intermediario
    for parte in partes_email[1:-1]:
        email_intermediario = f"{partes_email[0]}.{parte}@{dominio}"
        if email_intermediario not in emails_gerados:
            emails_gerados.add(email_intermediario)
            return email_intermediario

    # Se ainda existir, adiciona número
    sufixo = 1
    email_base = f"{partes_email[0]}.{partes_email[-1]}"
    while f"{email_base}{sufixo}@{dominio}" in emails_gerados:
        sufixo += 1

    email_final = f"{email_base}{sufixo}@{dominio}"
    emails_gerados.add(email_final)
    return email_final


# Função para verificar e criar e-mails e definir caminhos organizacionais
def verificar_e_criar_email(nome, tipo, df_base, emails_gerados, dominios, org_paths):
    # Trata tipo inválido
    if tipo not in dominios:
        tipo = None

    # Trata nome vazio / NaN
    if pd.isna(nome) or not str(nome).strip():
        return {
            'Nome Completo': '',
            'Email Address [Required]': 'NOME_INVALIDO',
            'First Name [Required]': '',
            'Last Name [Required]': '',
            'Org Unit Path [Required]': org_paths.get(tipo, org_paths[None]),
            'Status': 'NOME_VAZIO'
        }

    nome_formatado = remover_acentos(nome).strip().title()

    if not nome_formatado:
        return {
            'Nome Completo': '',
            'Email Address [Required]': 'NOME_INVALIDO',
            'First Name [Required]': '',
            'Last Name [Required]': '',
            'Org Unit Path [Required]': org_paths.get(tipo, org_paths[None]),
            'Status': 'NOME_INVALIDO'
        }

    nome_sem_acentos = nome_formatado.lower().strip()
    nome_comparacao = df_base['Nome Completo'].fillna('').apply(
        lambda x: remover_acentos(x).lower().strip()
    )

    # Se já existe na base
    if nome_sem_acentos in nome_comparacao.values:
        usuario_existente = df_base[nome_comparacao == nome_sem_acentos].iloc[0].to_dict()
        usuario_existente['Org Unit Path [Required]'] = org_paths.get(tipo, org_paths[None])

        # Garantir colunas no retorno
        if 'First Name [Required]' not in usuario_existente:
            partes_existente = nome_formatado.split()
            usuario_existente['First Name [Required]'] = partes_existente[0] if partes_existente else ''
        if 'Last Name [Required]' not in usuario_existente:
            partes_existente = nome_formatado.split()
            usuario_existente['Last Name [Required]'] = ' '.join(partes_existente[1:]) if len(partes_existente) > 1 else ''

        return usuario_existente

    # Novo usuário
    partes = nome_formatado.split()

    if not partes:
        return {
            'Nome Completo': nome_formatado,
            'Email Address [Required]': 'NOME_INVALIDO',
            'First Name [Required]': '',
            'Last Name [Required]': '',
            'Org Unit Path [Required]': org_paths.get(tipo, org_paths[None]),
            'Status': 'SEM_PARTES_VALIDAS'
        }

    email = gerar_email(partes, emails_gerados, dominios.get(tipo, dominios[None]))

    if not email:
        return {
            'Nome Completo': nome_formatado,
            'Email Address [Required]': 'EMAIL_NAO_GERADO',
            'First Name [Required]': partes[0] if partes else '',
            'Last Name [Required]': ' '.join(partes[1:]) if len(partes) > 1 else '',
            'Org Unit Path [Required]': org_paths.get(tipo, org_paths[None]),
            'Status': 'NOME_INVALIDO_PARA_EMAIL'
        }

    novo_usuario = {
        'Nome Completo': nome_formatado,
        'Email Address [Required]': email,
        'First Name [Required]': partes[0] if partes else '',
        'Last Name [Required]': ' '.join(partes[1:]) if len(partes) > 1 else '',
        'Org Unit Path [Required]': org_paths.get(tipo, org_paths[None]),
        'Status': 'NOVO'
    }

    return novo_usuario


# Função para converter DataFrame para Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output.getvalue()


# Função principal do Streamlit
def main():
    st.title('Criação de E-mails Institucionais')

    uploaded_file_base = st.file_uploader("Carregar arquivo base (base.xlsx):", type='xlsx')
    uploaded_file_teste = st.file_uploader("Carregar arquivo com os dados (dados.xlsx):", type='xlsx')

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
        'PROFESSOR': f"{prefixo_professor}.{dominio_padrao}",
        'ALUNO': f"{prefixo_aluno}.{dominio_padrao}",
    }

    org_paths = {
        None: org_padrao,
        'PROFESSOR': org_professor,
        'ALUNO': org_alunos,
    }

    if st.button('Processar Dados'):
        if uploaded_file_base is not None and uploaded_file_teste is not None:
            try:
                df_base = pd.read_excel(uploaded_file_base)
                df_teste = pd.read_excel(uploaded_file_teste)

                # Monta nome completo da base
                first_name_col = 'First Name [Required]'
                last_name_col = 'Last Name [Required]'

                if first_name_col not in df_base.columns:
                    df_base[first_name_col] = ''
                if last_name_col not in df_base.columns:
                    df_base[last_name_col] = ''

                df_base['Nome Completo'] = (
                    df_base[first_name_col].fillna('').astype(str).str.strip() + ' ' +
                    df_base[last_name_col].fillna('').astype(str).str.strip()
                ).str.strip()

                # Status opcional
                if 'Last Sign In [READ ONLY]' in df_base.columns:
                    df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(
                        lambda x: 'DESATIVADO' if str(x).strip() == 'Never logged in' else 'ATIVADO'
                    )
                else:
                    df_base['Status'] = ''

                # Garante colunas mínimas
                if 'Email Address [Required]' not in df_base.columns:
                    df_base['Email Address [Required]'] = ''
                if 'Org Unit Path [Required]' not in df_base.columns:
                    df_base['Org Unit Path [Required]'] = ''

                df_base = df_base[
                    ['Nome Completo', 'Email Address [Required]', 'Status', 'Org Unit Path [Required]']
                ].copy()

                emails_gerados = set(
                    df_base['Email Address [Required]']
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .tolist()
                )

                resultados = []

                # Detecta coluna de nome
                coluna_nome = None
                for c in ['Nome', 'NOME', 'Nome Completo', 'nome']:
                    if c in df_teste.columns:
                        coluna_nome = c
                        break

                if coluna_nome is None:
                    st.error("A planilha de dados não possui coluna de nome. Use uma coluna como 'Nome'.")
                    return

                for _, row in df_teste.iterrows():
                    tipo_usuario = (
                        str(row['Tipo']).strip().upper()
                        if 'Tipo' in df_teste.columns and not pd.isna(row['Tipo'])
                        else None
                    )

                    resultado = verificar_e_criar_email(
                        row[coluna_nome],
                        tipo_usuario,
                        df_base,
                        emails_gerados,
                        dominios,
                        org_paths
                    )
                    resultados.append(resultado)

                df_resultado_final = pd.DataFrame(resultados)

                if not df_resultado_final.empty:
                    excel_data = convert_df_to_excel(df_resultado_final)
                    st.success("Dados processados com sucesso.")
                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_data,
                        file_name="resultados_emails.xlsx",
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    st.dataframe(df_resultado_final)
                else:
                    st.error("DataFrame resultante está vazio, não há dados para exportar.")

            except Exception as e:
                st.error(f"Erro ao processar os dados: {e}")

        else:
            st.error("Por favor, carregue ambos os arquivos antes de processar.")


if __name__ == "__main__":
    main()