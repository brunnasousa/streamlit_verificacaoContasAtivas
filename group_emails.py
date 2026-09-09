import streamlit as st
import pandas as pd
from io import BytesIO

def main():
    st.title('Filtro e Ajuste de Dados de Grupos')

    # Upload do arquivo Excel
    uploaded_file = st.file_uploader("Upload seu arquivo Excel", type=['xlsx'])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        # Verifica se a coluna obrigatória existe
        if 'Email Address [Required]' not in df.columns:
            st.error("O arquivo não contém a coluna 'Email Address [Required]'. Verifique o formato do arquivo.")
            return
        
        # Criar coluna de domínio
        df['Domain'] = df['Email Address [Required]'].apply(lambda x: x.split('@')[-1])
        domains = df['Domain'].unique().tolist()

        # Seção para selecionar domínios de e-mail
        selected_domain = st.multiselect("Selecione os domínios", domains)

        if selected_domain:
            filtered_df = df[df['Domain'].isin(selected_domain)].copy()

            # Campo para inserir o Group Email
            group_email = st.text_input("Insira o Group Email [Required] para todos", "")
            if group_email:
                filtered_df['Group Email [Required]'] = group_email
            else:
                # Se o usuário não inserir um e-mail de grupo, definir um valor padrão
                filtered_df['Group Email [Required]'] = "group@example.com"

            # Campo para inserir o Member Role para todos
            default_role = st.text_input("Insira o Member Role padrão para todos", "MEMBER")
            filtered_df['Member Role'] = default_role
            
            # Definir todos como 'USER' no 'Member Type'
            filtered_df['Member Type'] = 'USER'

            # Criar a coluna 'Member Email' antes de preenchê-la
            filtered_df['Member Email'] = filtered_df.get('Member Email', pd.NA)

            # Preencher 'Member Email' com 'Email Address [Required]'
            if 'Email Address [Required]' in filtered_df.columns:
                filtered_df['Member Email'] = filtered_df['Email Address [Required]'].fillna(filtered_df['Member Email'])

            # Seção para inserir e-mails manualmente
            st.markdown("### Digite o e-mail e selecione o role correspondente (OWNER ou MANAGER)")
            custom_email_roles = []
            num_custom_emails = st.number_input("Quantos e-mails você deseja inserir?", min_value=1, value=1, step=1)

            for i in range(num_custom_emails):
                col1, col2 = st.columns(2)
                with col1:
                    custom_email = st.text_input(f"Email {i+1}", key=f"email_{i}")
                with col2:
                    custom_role = st.selectbox(f"Role {i+1}", ["OWNER", "MANAGER"], key=f"role_{i}")
                if custom_email:
                    custom_email_roles.append((custom_email, custom_role))

            # Criar DataFrame com os e-mails adicionados manualmente
            if custom_email_roles:
                new_rows = pd.DataFrame([{
                    'Group Email [Required]': group_email if group_email else "group@example.com",
                    'Member Email': custom_email,
                    'Member Type': 'USER',
                    'Member Role': custom_role
                } for custom_email, custom_role in custom_email_roles])

                # Concatenar os novos dados ao DataFrame existente
                filtered_df = pd.concat([filtered_df, new_rows], ignore_index=True)

            # **Garantir que as colunas obrigatórias existam antes de criar o arquivo final**
            required_columns = ['Group Email [Required]', 'Member Email', 'Member Type', 'Member Role']
            for col in required_columns:
                if col not in filtered_df.columns:
                    filtered_df[col] = ""

            final_df = filtered_df[required_columns].copy()

            # Gerar arquivo Excel para download
            output = BytesIO()
            final_df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(label="Baixar arquivo filtrado", 
                               data=output, 
                               file_name="filtered_grupo.xlsx", 
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.warning("Selecione pelo menos um domínio para prosseguir.")

if __name__ == "__main__":
    main()
