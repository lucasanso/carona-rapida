import streamlit as st
import jwt
import os
from time import sleep 
import pandas as pd


if "token" not in st.session_state:
    st.warning("Você não está autenticado(a).")
    sleep(3)
    st.switch_page("pages/login.py")

decode = jwt.decode(st.session_state.token, key=os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])

st.title(f"Olá, {decode.get("nome")}!")

with st.form("Formulário",border=True, clear_on_submit=True):
    st.markdown("#### Valor total: R$ 32,00")
    st.warning("Somatório da quantidade de caronas ainda não pagas")

    year_selected = st.selectbox(
        "Ano",
        options=["2026", "2025", "2024"],
        index=None,
        placeholder="Escolha um ano"
        )

    month_selected = st.selectbox(
        "Mês",
        options=["Janeiro", "Fevereiro", "Março"],
        index=None,
        placeholder="Escolha um mês"
        )
    
    pagas = st.checkbox("Exibir caronas pagas")

    st.form_submit_button("Consultar")

    if month_selected:
        dados_caronas = [
            {"Data": "02/03/2026", "Origem": "UFG - Campus Samambaia", "Destino": "Setor Bueno", "Valor": "R$ 7,00", "Motorista": "Lucas"},
            {"Data": "05/03/2026", "Origem": "Setor Bueno", "Destino": "UFG - Campus Samambaia", "Valor": "R$ 7,00", "Motorista": "Isabelle"},
            {"Data": "12/03/2026", "Origem": "Centro", "Destino": "UFG - Campus Samambaia", "Valor": "R$ 6,00", "Motorista": "Carlos"},
        ]
        
        df = pd.DataFrame(dados_caronas)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    
        