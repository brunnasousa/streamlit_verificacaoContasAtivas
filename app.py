#streamlit run app.py   
import streamlit as st
from verificacaoContasAtivas import main as verifica_main
from dadosResumidoAdmin import main as dados_main

# Definindo uma função para iniciar ou resetar a tela inicial
def set_initial_state():
    st.session_state.current_page = 'home'

# Verificando se o estado atual existe, se não, inicializa
if 'current_page' not in st.session_state:
    set_initial_state()

st.title('Bem-vindo ao Gerenciador de Contas')

# Adicionando os botões na barra lateral
if st.sidebar.button('Dados Resumidos do Admin'):
    st.session_state.current_page = 'dados'

if st.sidebar.button('Verificação de Contas Ativas'):
    st.session_state.current_page = 'verifica'

# Mostrando conteúdos baseados no estado
if st.session_state.current_page == 'verifica':
    verifica_main()
elif st.session_state.current_page == 'dados':
    dados_main()
elif st.session_state.current_page == 'home':
    st.write('Por favor, escolha uma opção ao lado para visualizar os dados.')


for _ in range(10):  # Ajuste o número baseado no tamanho da tela e conteúdo
    st.sidebar.write("")

# Assinatura no final da barra lateral
st.sidebar.markdown("---")
st.sidebar.markdown("*Feito por Brunna*", unsafe_allow_html=True)


# Feito por Brunna Sousa