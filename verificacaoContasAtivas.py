import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import date

def check_status(email, df_base):
    match = df_base[df_base['Email Address [Required]'] == email]['Last Sign In [READ ONLY]']
    if not match.empty:
        return 'DESATIVADO' if match.iloc[0] == 'Never logged in' else 'ATIVADA'
    else:
        return 'EMAIL NÃO ENCONTRADO'

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
        today = date.today().strftime("%d/%m/%Y")
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        worksheet.write(0, df.shape[1] - 1, f"Status {today}")
    processed_data = output.getvalue()
    return processed_data

def main():
    st.title('Análise de Status de uma lista de Emails')

    base_data_file = st.file_uploader("Upload sua base de dados:", type=['xlsx'], key="base_data_file")
    
    st.write("Certifique-se de que a lista de emails inclua a coluna 'Email'.")
    emails_to_check_file = st.file_uploader("Upload a lista de emails para verificar: ", type=['xlsx'], key="emails_to_check_file")
    

    if base_data_file and emails_to_check_file:
        df_base = pd.read_excel(base_data_file)
        df_emails_to_check = pd.read_excel(emails_to_check_file)

        # Verificar se a coluna 'Email' está presente
        if 'Email' not in df_emails_to_check.columns:
            st.error("O arquivo da lista para verificar deve conter uma coluna A denominada 'Email' como titulo")
            return

        email_column = 'Email'  # Supõe que a coluna com e-mails se chama 'Email'
        df_emails_to_check['Status'] = df_emails_to_check[email_column].apply(lambda email: check_status(email, df_base))

        status_counts = df_emails_to_check['Status'].value_counts()
        total_emails = df_emails_to_check.shape[0]

        status_counts_with_total = pd.concat([status_counts, pd.Series([total_emails], index=['TOTAL'])])
        status_percentage = (status_counts / total_emails) * 100
        status_percentage_with_total = pd.concat([status_percentage, pd.Series([100.0], index=['TOTAL'])])

        summary_df = pd.DataFrame({
            'Status': status_counts_with_total.index,
            'qtd': status_counts_with_total.values,
            'percentagem': status_percentage_with_total.values
        })

        st.markdown("### Resultado:")
        st.dataframe(summary_df.style.format({'percentagem': "{:.1f} %"}))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Quantitativo de Status')
            fig_quant = px.bar(status_counts, title="Quantidade por Status")
            st.plotly_chart(fig_quant, use_container_width=True)

        with col2:
            st.subheader('Porcentagem de Status')
            pie_data = pd.DataFrame({
                'Status': status_percentage.index,
                'Percentagem': status_percentage.values
            })
            fig_perc = px.pie(pie_data, values='Percentagem', names='Status', title='Porcentagem por Status')
            st.plotly_chart(fig_perc, use_container_width=True)

        st.subheader('Status dos Emails')
        st.write(df_emails_to_check[[email_column, 'Status']])

        excel_data = convert_df_to_excel(df_emails_to_check[[email_column, 'Status']])
        st.download_button(label="📥 Download Excel",
                           data=excel_data,
                           file_name="status_emails.xlsx",
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    main()

# Feito por Brunna Sousa