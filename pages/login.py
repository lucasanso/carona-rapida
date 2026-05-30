import streamlit as st
from requests import post
import jwt
import os
from dotenv import load_dotenv
from time import sleep
from jwt.exceptions import DecodeError

load_dotenv()

st.session_state.login = False
st.session_state.incorrect = False

st.title("Bem-vindo (a)!")

with st.container(border=True):
    st.subheader("Login")
    
    nome_usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
    senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
    
    st.markdown(" ")
    
    col_entrar, col_cadastrar, col_vazia = st.columns([0.8, 1.4, 4])

    with col_entrar:
        if st.button("Entrar"):
            if nome_usuario and senha:
                try:
                    payload = {
                        "nome_usuario": nome_usuario,
                        "senha": senha
                    }
                    
                    response = post("http://localhost:8000/passageiros/login", json=payload)

                    if response.status_code == 200:
                        dados = response.json()
                        token = jwt.decode(dados.get("token"), os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
                        
                        
                        st.session_state.login = True
                        st.session_state.token = dados.get("token")

                    else:
                        st.error(f"Erro [{response.status_code}] {response.json()}")
                except DecodeError:
                    st.session_state.incorrect = True

            else:
                st.warning("Preencha todos os campos.")

    with col_cadastrar:
        if st.button("Cadastrar-se"):
            st.switch_page("pages/cadastrar.py")

if st.session_state.login:
    st.success("Login realizado com sucesso!")
    sleep(2)
    st.switch_page("pages/consulta.py")

if st.session_state.incorrect:
    st.error("Credenciais inválidas.")
    sleep(2)
    st.rerun()