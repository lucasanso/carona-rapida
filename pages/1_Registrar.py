import streamlit as st
from requests import get, post, ConnectionError
from streamlit import errors
from time import sleep

if "token" not in st.session_state:
    st.warning("Você não está autenticado")
    sleep(1.5)
    st.switch_page("Inicial.py")

if "erro_api" not in st.session_state:
    st.session_state.erro_api = None
if "sucesso_api" not in st.session_state:
    st.session_state.sucesso_api = None

with st.sidebar:
    st.title("Opções")
    st.selectbox("Selecione uma opção", ["Registrar pagamento", "Atualizar informações"])

st.title("Caronas UFG")
lista = []

try:
    resposta = get("http://localhost:8000/passageiros")
    if resposta.status_code == 200:
        dados = resposta.json()
        lista = [p[0] for p in dados.get('passengers', [])]
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
                st.session_state.sucesso_api = "Carona registrada!"
            else:
                dados_erro = response.json()
                st.session_state.erro_api = dados_erro.get("detail", "Erro desconhecido na API.")
        except ConnectionError:
            st.session_state.erro_api = "Não foi possível conectar ao servidor backend."

        st.rerun()

if st.session_state.erro_api:
    st.error(st.session_state.erro_api)

if st.session_state.sucesso_api:
    st.success(st.session_state.sucesso_api)