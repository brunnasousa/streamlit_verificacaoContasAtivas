import streamlit as st

def main():
    # Definir as opções para desinstalar apps
    uninstall_options = {
        "Inteceleri Geometa": "adb uninstall com.Inteceleri.Geometa",
        "Matematicando Full Olimpiadas": "adb shell pm uninstall -k --user 0 air.MatematicandoFull",
        "Matematicando tradicional": "adb shell pm uninstall -k --user 0 air.MatematicandoEducation"
    }

    # Função para gerar o arquivo .bat com as seleções
    def gerar_bat_file(uninstall_selection, install_apps):
        bat_script = "@echo off\n:start\n"
        
        if uninstall_selection:
            bat_script += "echo Uninstalling apps...\n"
            for app_command in uninstall_selection:
                bat_script += app_command + "\n"
        
        if install_apps:
            bat_script += "\necho Installing apps...\n"
            for app_name, app_path in install_apps:
                bat_script += f"echo Installing {app_name}...\nadb install {app_path}\n"
        
        bat_script += """
        echo All tasks completed.
        echo.
        echo Pressione "c" para executar novamente ou qualquer outra tecla para sair.
        set /p input=Digite sua escolha: 
        if /i "%input%"=="c" goto start

        echo Saindo...
        pause
        """
        
        # Criar arquivo .bat
        with open("script_instalar_desinstalar.bat", "w") as file:
            file.write(bat_script)
        
        return bat_script

    # Layout do Streamlit
    st.title("Gerador de Script .BAT para Instalar e Desinstalar Apps")

    # Checkboxes para desinstalação de apps
    st.markdown("### - Selecione os apps para desinstalar")
    uninstall_selection = []
    
    for app_name, app_command in uninstall_options.items():
        if st.checkbox(f"Desinstalar {app_name}"):
            uninstall_selection.append(app_command)

    # Definir uma lista vazia para apps que o usuário deseja instalar
    install_apps = []

    # Permitir que o usuário insira nome do app e caminho do APK
    st.markdown("### - Adicione os apps que deseja instalar")
    num_apps = st.number_input("Quantos apps você deseja instalar?", min_value=1, step=1)

    for i in range(num_apps):
        # Criando colunas para colocar os inputs lado a lado
        col1, col2 = st.columns(2)
        with col1:
            app_name = st.text_input(f"Nome do App {i+1}", f"APP{i+1}")
        with col2:
            app_path = st.text_input(f"Caminho do APK {i+1}", f"C:\\caminho\\do\\arquivo.apk")
        
        install_apps.append((app_name, app_path))

    # Botão para gerar o arquivo .bat
    if st.button("Gerar arquivo .BAT"):
        bat_script = gerar_bat_file(uninstall_selection, install_apps)
        st.success("Arquivo .bat gerado com sucesso!")
        
        # Botão para baixar o arquivo .bat
        st.download_button(label="Baixar arquivo .BAT", 
                           data=bat_script, 
                           file_name="script_instalar_desinstalar.bat",
                           mime="application/octet-stream")

        # Exibir o script gerado e fornecer a opção de copiar
        st.text_area("Script .BAT gerado: executar como administrador", bat_script, height=300)
        st.write("ATENÇÃO: Precisa ter o 'adb' instalado no computador e a função 'desenvolvedor' + 'depuração usb' no celular ativo.")

# Certifique-se de que o código funcione apenas ao rodar o script diretamente
if __name__ == "__main__":
    main()
