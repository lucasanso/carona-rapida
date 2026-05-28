import streamlit as st

st.title("Cadastro de passageiro")

with st.container(border=True):
    nome = st.text_input("Nome", placeholder="Digite seu nome")
    sobrenome = st.text_input("Sobrenome", placeholder="Digite seu sobrenome")
    usuario = st.text_input("Usuário", placeholder="Digite seu nome de usuário")
    telefone = st.text_input("Telefone", placeholder="6299999999")
    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
    senha_confirm = st.text_input("Digite sua senha novamente", type="password")

    st.markdown(" ")

    col_cadastrar, col_login, col_vazia = st.columns([1, 1.2, 3])

    with col_cadastrar:
        if st.button("Cadastrar-se"):
            if nome and sobrenome and usuario and telefone and senha and senha_confirm:
                if senha == senha_confirm:
                    st.success("Cadastro realizado com sucesso!")
                else:
                    st.error("As senhas não coincidem.")
            else:
                st.warning("Por favor, preencha todos os campos.")
        
    with col_login:
        if st.button("Fazer login"):
            st.switch_page("Inicial.py") 