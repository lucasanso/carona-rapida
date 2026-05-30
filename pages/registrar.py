import streamlit as st
from requests import get, post, ConnectionError
from time import sleep
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

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


if "erro_api" not in st.session_state:
    st.session_state.erro_api = None
if "sucesso_api" not in st.session_state:
    st.session_state.sucesso_api = None


st.title("Caronas UFG")
lista = []

try:
    resposta = get("http://localhost:8000/passageiros")
    if resposta.status_code == 200:
        dados = resposta.json()
        lista = [p[1] for p in dados.get('passengers', [])]
    else:
        st.warning("Não foi possível carregar os passageiros da API.")
except ConnectionError:
    st.warning("Não foi possível conectar ao servidor para buscar passageiros.")

with st.form("formulario", clear_on_submit=False):
    st.subheader("Registro de carona")

    passageiros = st.multiselect("Passageiros", placeholder="Nome", options=lista)
    data = st.date_input("Data")
    tipo_carona = st.selectbox("Tipo da carona", ["Ida", "Volta"])
    enviar = st.form_submit_button("Enviar")

    if tipo_carona == "Ida":
        tipo_carona = 1
    else:
        tipo_carona = 2

    # payload
    payload = {
        "data_carona" : str(data),
        "tipo_carona": tipo_carona,
        "passageiros": passageiros
    }

    if enviar:
        st.session_state.erro_api = None
        st.session_state.sucesso_api = None

        try:
            response = post("http://localhost:8000/caronas/registrar", json=payload)
            if response.status_code == 200:
                st.toast("Carona registrada com sucesso!")
                sleep(1.5)
                st.rerun()
            else:
                try:
                    dados_erro = response.json()
                    erro_msg = dados_erro.get("detail", "Erro desconhecido na API.")
                except Exception:
                    erro_msg = f"Erro interno no servidor da API (Status {response.status_code})."
                
                st.error(erro_msg)
                sleep(1.5)
                st.rerun()

        except ConnectionError:
            st.session_state.erro_api = "Não foi possível conectar ao servidor backend."
            sleep(1.2)
            st.rerun()