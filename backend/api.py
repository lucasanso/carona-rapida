from psycopg2 import Error, connect
import os
from dotenv import load_dotenv
import json
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status

load_dotenv()

class PostgresConnect:
    def __init__(self):
        self.conexao = self.connecting()

    def connecting(self):
        try:
            conexao = connect(
                user = os.getenv("POSTGRES_USER"),
                password = os.getenv("POSTGRES_PASS"),
                database=os.getenv("POSTGRES_DB"),
                host="localhost"
            )

            print("[SUCESSO] Conexão realizada com sucesso")

            return conexao
        
        except Error as e:
            print(f"Erro ao conectar no PostgreSQL: {e}")

db = PostgresConnect()

class CaronaSchema(BaseModel):
    data_carona: str
    tipo_carona: int
    passageiros: List[str]

app = FastAPI()


@app.get("/passengers")
def get_passengers():
    query = """
            SELECT nome FROM passageiros;
            """
    try:
        cursor = db.conexao.cursor()
        cursor.execute(query)
        
        lista = {
            "passengers" : cursor.fetchall()
        }
        cursor.close()

        return lista
    
    except Error as e:
        db.conexao.rollback()
        return {
            "response" : e
        }

# Cadastrar carona    
@app.post("/carona")
def cadastrar_carona(carona: CaronaSchema):
    mapping = {
        "Beatriz": 3,
        "Luiz Fernando": 1,
        "Kassia Fernanda": 2,
        "Patrick": 4,
        "Melqui": 5,
        "Myllena": 6
    }

    query = """
            INSERT INTO caronas(data_carona, tipo_carona) VALUES (%s, %s) RETURNING ID;
            """
    
    query_2 = """
            INSERT INTO passageiro_carona(id_passageiro, id_carona, paga) VALUES (%s, %s, %s);
            """
    try:
        cursor = db.conexao.cursor()

        cursor.execute(query, (carona.data_carona, carona.tipo_carona))
        resultado = cursor.fetchone()
        id_carona = resultado[0] if resultado else None

        for passenger in carona.passageiros:
            cursor.execute(query_2, (mapping[passenger], id_carona, False))
            print(f"Inseri o(a): {mapping[passenger]}")
    
        db.conexao.commit()
        cursor.close()

        return {
            "status": "Sucesso",
            "content": carona.model_dump_json(),
            "id_carona": id_carona
        }

    except Error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Essa carona já foi computada."
        )
    

