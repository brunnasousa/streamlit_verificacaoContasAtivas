import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import plotly.graph_objects as go

def process_data(df_base):
    df_base['Full Name'] = df_base['First Name [Required]'] + ' ' + df_base['Last Name [Required]']
    df_base['Status'] = df_base['Last Sign In [READ ONLY]'].apply(lambda x: 'DESATIVADO' if x == 'Never logged in' else 'ATIVO')
    columns_to_include = ['Full Name', 'Email Address [Required]', 'Status']
    if 'Org Unit Path [Required]' in df_base.columns:
        columns_to_include.append('Org Unit Path [Required]')
    return df_base[columns_to_include]

def display_statistics(df_base):
    total_count = df_base.shape[0]
    status_counts = df_base['Status'].value_counts()
    status_percentage = (status_counts / total_count) * 100
    status_summary = pd.DataFrame({
        'Status': status_counts.index,
        'qtd': status_counts.values,
        'percentagem': status_percentage.values
    })
    # Adicionando linha 'TOTAL' apenas para a tabela, não para os gráficos
    status_summary_with_total = status_summary.copy()
    status_summary_with_total.loc[len(status_summary_with_total.index)] = ['TOTAL', total_count, 100.0]

    st.subheader("1 - Contagem e Porcentagem de Status Geral:")
    st.dataframe(status_summary_with_total.style.format({'percentagem': "{:.2f}%"}))

    # Usando dados sem 'TOTAL' para os gráficos
    col1, col2 = st.columns(2)
    with col1:
        fig_quant = px.bar(status_summary, x='Status', y='qtd', title="Quantidade por Status")
        st.plotly_chart(fig_quant, use_container_width=True)
    with col2:
        fig_perc = px.pie(status_summary, values='percentagem', names='Status', title='Porcentagem por Status')
        st.plotly_chart(fig_perc, use_container_width=True)


    ##### 2 
    if 'Org Unit Path [Required]' in df_base.columns:
        org_unit_counts = df_base['Org Unit Path [Required]'].value_counts()
        org_unit_percentage = (org_unit_counts / total_count) * 100
        org_summary = pd.DataFrame({
            'Org Unit Path': org_unit_counts.index,
            'qtd': org_unit_counts.values,
            'percentagem': org_unit_percentage.values
        })
        org_summary.loc[len(org_summary.index)] = ['TOTAL', total_count, 100.0]

        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("2 - Contagem e Porcentagem por Org Unit Path:")
            st.dataframe(org_summary.style.format({'percentagem': "{:.2f}%"}))
        with col2:
            fig_perc_path = px.pie(org_summary[org_summary['Org Unit Path'] != 'TOTAL'], values='percentagem', names='Org Unit Path', title='Porcentagem por Org Unit Path')
            st.plotly_chart(fig_perc_path, use_container_width=True)


        org_summary_filtered = org_summary[org_summary['Org Unit Path'] != 'TOTAL']  # Filtrando 'TOTAL'
        fig_quant_path = px.bar(org_summary_filtered, x='Org Unit Path', y='qtd', title="Quantidade por Org Unit Path")
        st.plotly_chart(fig_quant_path)

        # Criando uma única tabela para todos os dados de 'Org Unit Path'
        all_status_by_path = pd.DataFrame(columns=['Org Unit Path', 'Status', 'qtd', 'percentagem'])
        for path, data in df_base.groupby('Org Unit Path [Required]'):
            status_by_path = pd.DataFrame({
                'Status': data['Status'].value_counts().index,
                'qtd': data['Status'].value_counts().values,
                'percentagem': (data['Status'].value_counts() / data.shape[0] * 100).values,
                'Org Unit Path': path
            })
            all_status_by_path = pd.concat([all_status_by_path, status_by_path])

            # Adicionando uma linha total para cada grupo
            total_row = pd.DataFrame({
                'Status': ['TOTAL'],
                'qtd': [data.shape[0]],
                'percentagem': [100.0],
                'Org Unit Path': [path]
            })
            all_status_by_path = pd.concat([all_status_by_path, total_row])

        # Exibindo a tabela única
        st.subheader("3 - Contagem e Porcentagem de Status por Org Unit Path:")
        st.dataframe(all_status_by_path.style.format({'percentagem': "{:.2f}%"}))

    


def main():
    st.title('Análise de Dados Administrativos')
    uploaded_file = st.file_uploader("Upload sua base de dados:", type=['xlsx'], key="unique_key_for_admin")

    if uploaded_file is not None:
        df_base = pd.read_excel(uploaded_file)
        df_final = process_data(df_base)
        
        # Download do DataFrame final para Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_final.to_excel(writer, index=False)
            writer.book.close()
        output.seek(0)
        st.download_button(label="📥 Download Excel", data=output, file_name="usuarios_filtrados.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        display_statistics(df_base)
        
if __name__ == "__main__":
    main()
