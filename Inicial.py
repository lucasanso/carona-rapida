import streamlit as st
from requests import get, post
import jwt
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv()


st.set_page_config(
    page_title="Caronas UFG",
    page_icon="👋",

)

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
                payload = {
                    "nome_usuario": nome_usuario,
                    "senha": senha
                }
                
                response = post("http://localhost:8000/passageiros/login", json=payload)

                if response.status_code == 200:
                    dados = response.json()
                    token = jwt.decode(dados.get("token"), os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
                    
                    st.success(f"Totalmente conectado! Bem vindo(a) {token.get('nome')}")
                    # # st.session_state.token = dados.get("token")
                    
                    sleep(1)

                    st.switch_page("pages/1_Registrar.py")

                else:
                    st.error(f"Erro [{response.status_code}] {response.json()}")
            else:
                st.warning("Preencha todos os campos.")
                
    with col_cadastrar:
        if st.button("Cadastrar-se"):
            st.switch_page("pages/2_Cadastrar.py")