import streamlit as st
from requests import post


st.title("Cadastro de passageiro")
with st.container(border=True):
    st.subheader("Insira suas informações")
    nome = st.text_input("Nome", placeholder="Digite seu nome")
    sobrenome = st.text_input("Sobrenome", placeholder="Digite seu sobrenome")
    nome_usuario = st.text_input("Usuário", placeholder="Digite seu nome de usuário")
    telefone = st.text_input("Telefone", placeholder="6299999999")
    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
    senha_confirm = st.text_input("Digite sua senha novamente", type="password")

    st.markdown(" ")

    col_cadastrar, col_login, col_vazia = st.columns([1, 1.2, 3])

    with col_cadastrar:
        if st.button("Cadastrar-se"):
            if nome and sobrenome and nome_usuario and telefone and senha and senha_confirm:
                payload = {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "nome_usuario": nome_usuario,
                    "senha": senha,
                    "telefone": telefone,
                }

                response = post("http://fastapi/passageiros/cadastrar", json=payload)
                
                if senha == senha_confirm and response.status_code == 200:
                    st.success("Cadastro realizado com sucesso!")
                else:
                    st.error("As senhas não coincidem.")
            else:
                st.warning("Por favor, preencha todos os campos.")
        
    with col_login:
        if st.button("Fazer login"):
            st.switch_page("pages/login.py") 