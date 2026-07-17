from fastapi import APIRouter, HTTPException, status
from typing import List
from pydantic import BaseModel
from psycopg2 import connect, Error, errors
import os
from dotenv import load_dotenv
from init_db import PostgresInit

load_dotenv()

router = APIRouter(prefix="/caronas", tags=["Gerenciamento de Caronas"])

class CaronaSchema(BaseModel):
    data_carona: str
    tipo_carona: int
    passageiros: List[str]

class PostgresConnect:
    def __init__(self):
        self.conexao = self.connecting()

    def connecting(self):
        try:
            return connect(
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASS"),
                database=os.getenv("POSTGRES_DB"),
                host="carona-db"
            )
        except Error as e:
            print(f"[ERRO] Falha crítica ao conectar no PostgreSQL: {e}")
            return None

db = PostgresConnect()

MAPA_PASSAGEIROS = {
    "Beatriz": 3, "Luiz Fernando": 10, "Kassia Fernanda": 2,
    "Patrick": 4, "Melqui": 5, "Myllena": 6, "Lucas": 1, "Ana Rute": 2
}


@router.get("/cria-banco")
def criar_banco():
    executar = PostgresInit()
    executar()
    

@router.post("/registrar")
def cadastrar_carona(carona: CaronaSchema):
    if not db.conexao or db.conexao.closed:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de banco de dados indisponível no momento."
        )

    for passenger in carona.passageiros:
        if passenger not in MAPA_PASSAGEIROS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Passageiro '{passenger}' não está cadastrado no sistema."
            )

    query_carona = "INSERT INTO caronas(data_carona, tipo_carona) VALUES (%s, %s) RETURNING ID;"
    query_vinculo = "INSERT INTO passageiro_carona(id_passageiro, id_carona, paga) VALUES (%s, %s, %s);"
    
    cursor = None
    try:
        cursor = db.conexao.cursor()

        cursor.execute(query_carona, (carona.data_carona, carona.tipo_carona))
        id_carona = cursor.fetchone()[0]
        
        for passenger in carona.passageiros:
            id_passageiro = MAPA_PASSAGEIROS[passenger]
            cursor.execute(query_vinculo, (id_passageiro, id_carona, False))
    
        db.conexao.commit()
        
        return {
            "status": "Sucesso",
            "id_carona": id_carona,
            "message": "Carona e passageiros registrados com sucesso."
        }

    except errors.UniqueViolation:
        db.conexao.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta carona já foi computada (registro duplicado)."
        )
        
    except errors.ForeignKeyViolation:
        db.conexao.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de consistência: ID de passageiro inexistente no banco."
        )

    except Error as e:
        if db.conexao:
            db.conexao.rollback()
        print(f"[ERRO BANCO]: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a transação no banco de dados."
        )
        
    except Exception as e:
        if db.conexao:
            db.conexao.rollback()
        print(f"[ERRO PYTHON]: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro inesperado no servidor."
        )
        
    finally:
        if cursor:
            cursor.close()