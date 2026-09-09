#streamlit run app.py   
import streamlit as st

# Importando suas funções dos módulos
from verificacaoContasAtivas import main as verifica_main
from dadosResumidoAdmin import main as dados_main
from email_creation import main as email_creation_main
from instalar_desinstalarApps import main as script_apps_main
from group_emails import main as script_group_main

# Inicialização ou reinicialização da tela inicial
def set_initial_state():
    st.session_state.current_page = 'home'

if 'current_page' not in st.session_state:
    set_initial_state()

# Adicionando os botões na barra lateral
if st.sidebar.button('Dados Resumidos do Admin'):  #dadosResumidoAdmin.py
    st.session_state.current_page = 'dados'

if st.sidebar.button('Verificação de Contas Ativas'): #verificacaoContasAtivas.py
    st.session_state.current_page = 'verifica'

if st.sidebar.button('Criação de E-mails Institucionais'): #email_creation.py
    st.session_state.current_page = 'create_email'

if st.sidebar.button('script BAT Instalar e Desinstalar apps'): #instalar_desinstalarApps.py
    st.session_state.current_page = 'script_apps'

if st.sidebar.button('script atualização de grupos'): #group-emails.py
    st.session_state.current_page = 'script_groups'


# Mostrando conteúdos baseados no estado
if st.session_state.current_page == 'verifica':
    verifica_main()
elif st.session_state.current_page == 'dados':
    dados_main()
elif st.session_state.current_page == 'create_email':
    email_creation_main()
elif st.session_state.current_page == 'script_apps':
    script_apps_main()
elif st.session_state.current_page == 'script_groups':
    script_group_main()

elif st.session_state.current_page == 'home':
    st.title('Inteceleri')
    st.write('escolha uma opção ao lado.')
    


if st.session_state.current_page == 'home':
    st.write('______')

    # Seção de explicação
    st.markdown("#### Dados Resumidos do Admin")
    with st.expander("Manual: Dados resumidos das principais informações de administração do sistema."):
        st.write("""
        1. Baixar do Google Admin: planilha com todos os dados dos usuários
        2. Fazer o upload na plataforma
                 
        """)

        #image_path = 'imagens/baixar-dados-usuarios-google-admin.png' 
        image_path = '/home/brunna_sousa/streamlit-dashboard/imagens/baixar-dados-usuarios-google-admin.png'
        st.image(image_path, caption='Google Admin', use_column_width=False, width=350)

    st.markdown("#### Verificação de Contas Ativas")
    with st.expander("Fazemos upload de uma lista de email e ele vai dizer quais usuários ativaram ou quais permanecem desativados"):
        st.write("""
        1. Upload sua base de dados (**Arquivo 1**): Base de dados do Google Admin com os dados dos usuários.
        2. Upload a Lista de E-mails a Verificar (**Arquivo 2**):
                 
            2.1 - Fazer upload de um arquivo em Excel (.xlsx) sendo a primeira coluna com o titulo "Emails", e a lista de e-mail que ele deve analisar.
        """)
        
        #image_path = 'imagens/baixar-dados-usuarios-google-admin.png' 
        image_path = '/home/brunna_sousa/streamlit-dashboard/imagens/baixar-dados-usuarios-google-admin.png'
        st.image(image_path, caption='arquivo 1: Google Admin', use_column_width=False, width=350)

        #image_path = 'imagens/analise-emails.png' 
        image_path = '/home/brunna_sousa/streamlit-dashboard/imagens/analise-emails.png'
        st.image(image_path, caption='arquivo 2: upload excel', use_column_width=False, width=350)

    st.markdown("#### Criação de E-mails Institucionais")
    with st.expander("Como criar usúarios em massa e sem duplicação"):
        st.write("""
                 
        1- **Arquivo 1**: Fornecer a base de dados do Google Admin (tem que ser o completo).
                 

2- **Arquivo 2**: Upload do arquivo excel (.xlsx) com a coluna A escrito "Nome", e a coluna B escrito "Tipo":
	   
    2.1 Tipo: especificar se é Professor ou Aluno. 
	2.2 Caso seja servidor (com o domínio padrão) basta deixar em branco.
                 
3. Após configurar o domínio padrão + Unidade Organizacional
                 
4. Ele vai fornecer o excel com:
                 
    4.1 dizer se aquela pessoa já possui email institucional + Status (ativo ou desativado).
                 
    4.2 Aqueles que ainda não possuem e-email institucional: ele vai criar de acordo com o domínio fornecido e o tipo.
                 
    4.3 usuários com os mesmos sobrenomes ou com nome+sobrenome existente no dominio, ele vai pegar o proximo nome
        """)

        #image_path = 'imagens/baixar-dados-usuarios-google-admin.png' 
        image_path = '/home/brunna_sousa/streamlit-dashboard/imagens/baixar-dados-usuarios-google-admin.png'
        st.image(image_path, caption='arquivo 1: Google Admin', use_column_width=False, width=350)
        
        #image_path = 'imagens/criacao-de-contas-upload-arqv2.png' 
        image_path = '/home/brunna_sousa/streamlit-dashboard/imagens/criacao-de-contas-upload-arqv2.png'
        st.image(image_path, caption='Arquivo 2 de upload', use_column_width=True)

        #image_path = 'imagens/criacao-de-contas-final.png' 
        image_path = '/home/brunna_sousa/streamlit-dashboard/imagens/criacao-de-contas-final.png'
        st.image(image_path, caption='Resultado após o processamento', use_column_width=True)

    st.markdown("#### Script BAT Instalar e Desinstalar apps")
    with st.expander("Instruções para uso da ferramenta de geração de script .BAT"):
        st.write("""

        1 - Escolha os aplicativos que deseja desinstalar:

        1.1 Na seção "Selecione os apps para desinstalar", você verá uma lista de opções com checkboxes.
        1.2 Marque os aplicativos que deseja remover do sistema.
                 
       2 - Adicione os aplicativos que deseja instalar:

        2.1 Na seção "Adicione os apps que deseja instalar", insira o nome do aplicativo no primeiro campo e o caminho do arquivo APK do seu computador no segundo campo correspondente.
        2.2 Você pode adicionar quantos aplicativos quiser. Para isso, use o campo "Quantos apps você deseja instalar?" e ajuste o número.
                 
    3 - Gerar o script:

        3.1 Após fazer suas seleções e preencher as informações, clique no botão "Gerar arquivo .BAT".
        3.2 Um arquivo .BAT será gerado automaticamente com os comandos de instalação e desinstalação que você configurou.
        
    4 - Baixar ou copiar o script:

        4.1 Você verá o script gerado na tela. Pode copiá-lo diretamente ou baixar o arquivo .BAT clicando no botão "Baixar arquivo .BAT".
        4.2 O script estará pronto para ser executado no seu sistema Windows.
                 
    -- Observações:
    * Precisa ter o adb instalado no pc.
    * 'Modo desenvolvedor' e 'Depuração USB' tem que está ativo.
    * Executar o arquivo .bat como administrador
                 
        """)
        
        #image_path = 'imagens/tela-inicial-adb.png' 
        image_path = '/home/brunna_sousa/streamlit-dashboard/imagens/tela-inicial-adb.png'
        st.image(image_path, caption='Tela inicial do adb após executação, apertar "C" para continuar.', use_column_width=True)

    st.markdown("#### Script atualização de grupos")
    with st.expander("Filtro e Ajuste de Dados de Grupos em massa para o Google Workspace"):
        st.write("""

        1 - fazer o upload do arquivo excel com todos os dados do google workspace
                 
       2 - Selecionar qual será do grupo de email entre os dominios disponiveis

    3 - Escrever o email principal desse grupo de email

    4 - Escolher entre Manger e Owner.              
        """)


# Espaços adicionais na barra lateral, para estética
for _ in range(20):
    st.sidebar.write("")

# Assinatura no final da barra lateral
st.sidebar.markdown("---")
st.sidebar.markdown("*Desenvolvido por: Área Técnica - Inteceleri*", unsafe_allow_html=True)
