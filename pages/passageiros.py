import streamlit as st
from time import sleep
import jwt
import os

if "token" not in st.session_state:
    st.warning("Você não está autenticado(a).")
    sleep(3)
    st.switch_page("pages/login.py")

if st.session_state.token:
    decode = jwt.decode(st.session_state.token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])

    if decode.get("nome_usuario") != "admin":
        st.error("Você não tem esta permissão.")
        sleep(4)
        st.switch_page("pages/consulta.py")

st.title("Gestão de usuários")