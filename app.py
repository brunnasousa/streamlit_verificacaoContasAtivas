#streamlit run app.py   
import streamlit as st

# Importando suas funções dos módulos
from verificacaoContasAtivas import main as verifica_main
from dadosResumidoAdmin import main as dados_main
from email_creation import main as email_creation_main  # Certifique-se de ter este módulo configurado corretamente

# Inicialização ou reinicialização da tela inicial
def set_initial_state():
    st.session_state.current_page = 'home'

# Verificar se o estado atual existe, se não, inicializar
if 'current_page' not in st.session_state:
    set_initial_state()

st.title('Bem-vindo ao Gerenciador de Contas')

# Adicionando os botões na barra lateral
if st.sidebar.button('Dados Resumidos do Admin'):
    st.session_state.current_page = 'dados'

if st.sidebar.button('Verificação de Contas Ativas'):
    st.session_state.current_page = 'verifica'

if st.sidebar.button('Criação de E-mails Institucionais'):
    st.session_state.current_page = 'create_email'

# Mostrando conteúdos baseados no estado
if st.session_state.current_page == 'verifica':
    verifica_main()
elif st.session_state.current_page == 'dados':
    dados_main()
elif st.session_state.current_page == 'create_email':
    email_creation_main()  # Chamando a função principal do seu novo módulo
elif st.session_state.current_page == 'home':
    st.write('Por favor, escolha uma opção ao lado para visualizar os dados.')

# Espaços adicionais na barra lateral, para estética
for _ in range(10):
    st.sidebar.write("")

# Assinatura no final da barra lateral
st.sidebar.markdown("---")
st.sidebar.markdown("*Feito por Brunna*", unsafe_allow_html=True)



# Feito por Brunna Sousa