import streamlit as st

st.set_page_config(page_title="Caronas UFG",  layout="centered")

pagina_home = st.Page(
    page="pages/login.py", 
    title="Login", 
    icon=":material/home:", 
    default=True 
)

pagina_caronas = st.Page(
    page="pages/registrar.py", 
    title="Gerenciar caronas", 
    icon=":material/directions_car:"
)

pagina_passageiros = st.Page(
    page="pages/cadastrar.py", 
    title="Cadastrar-se", 
    icon=":material/group:",
)

pagina_consulta =  st.Page(
    page="pages/consulta.py", 
    title="Consultar caronas", 
    icon=":material/search:"
)

pagina_perfil = st.Page(
    page="pages/passageiros.py",
    title="Gerenciar passageiros",
    icon=":material/person:", 
)

navegacao = st.navigation(
    {
        "Início": [pagina_home, pagina_passageiros],
        "Usuário" : [pagina_consulta],
        "Administração": [pagina_caronas, pagina_perfil],
    }
)

navegacao.run()