from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel
from psycopg2 import connect, Error
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/caronas",
    tags=["Gerenciamento de Caronas"]
)

class CaronaSchema(BaseModel):
    data_carona: str
    tipo_carona: int
    passageiros: List[str]


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

@router.post("/registrar")
def cadastrar_carona(carona: CaronaSchema):
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
        mappping = os.getenv("MAPPING")
        for passenger in carona.passageiros:
            cursor.execute(query_2, (mappping[passenger], id_carona, False))
    
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