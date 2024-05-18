import pandas as pd
import unicodedata
import streamlit as st
from io import BytesIO
#cod
def remover_acentos(texto):
    """Remove acentos do texto utilizando a normalização Unicode."""
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

def gerar_email(partes, emails_gerados, dominio):
    """Gera um endereço de email único baseado nas partes do nome fornecido e no domínio."""
    excluidas = ['de', 'dos', 'da', 'do', 'com']
    partes_email = [remover_acentos(parte).lower() for parte in partes if parte.lower() not in excluidas and parte.isalpha()]
    email = f"{partes_email[0]}.{partes_email[-1]}@{dominio}"
    if email not in emails_gerados:
        return email
    for parte in partes_email[1:-1]:
        email_intermediario = f"{partes_email[0]}.{parte}@{dominio}"
        if email_intermediario not in emails_gerados:
            return email_intermediario
    sufixo = 1
    email_base = f"{partes_email[0]}.{partes_email[-1]}"
    while f"{email_base}{sufixo}@{dominio}" in emails_gerados:
        sufixo += 1
    return f"{email_base}{sufixo}@{dominio}"

def convert_df_to_excel(df):
    """Converts a DataFrame to an Excel file stored in a BytesIO stream."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
    output.seek(0)
    return output.getvalue()

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

    dominio_professor = prefixo_professor + '.' + dominio_padrao
    dominio_aluno = prefixo_aluno + '.' + dominio_padrao
    st.text(f"Domínio para Padrão: {dominio_padrao}")
    st.text(f"Domínio para Professores: {dominio_professor}")
    st.text(f"Domínio para Alunos: {dominio_aluno}")

    if st.button('Processar Dados'):
        if uploaded_file_base is not None and uploaded_file_teste is not None:
            df_base = pd.read_excel(uploaded_file_base)
            df_teste = pd.read_excel(uploaded_file_teste)
            
            # Aqui você pode continuar com o processamento dos dados
            df_resultado = df_teste  # Substitua esta linha pela sua lógica de processamento real
            
            if not df_resultado.empty:
                excel_data = convert_df_to_excel(df_resultado)
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
