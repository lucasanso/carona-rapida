from fastapi import APIRouter, HTTPException, status
from psycopg2 import connect, Error
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import bcrypt
import jwt
from datetime import timedelta, datetime

load_dotenv()

router = APIRouter(
    prefix="/passageiros",
    tags=["Gerenciamento de Passageiros"]
)

class LoginSchema(BaseModel):
    nome_usuario: str
    senha: str

class PassageiroSchema(BaseModel):
    nome: str
    sobrenome: str
    telefone: str
    senha: str
    nome_usuario: str

def verifica_senha(senha_digitada: str, senha_banco: str):
    teste = senha_digitada.encode('utf-8')
    senha_banco_bytes = senha_banco.encode('utf-8')

    return bcrypt.checkpw(teste, senha_banco_bytes)

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

@router.post("/cadastrar")
def cadastrar_passageiro(passageiro: PassageiroSchema):
    query = """
            INSERT INTO passageiros(nome, sobrenome, nome_usuario, senha, telefone) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (telefone) DO NOTHING;
            """

    try:
        cursor = db.conexao.cursor()
        
        password = passageiro.senha.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        
        senha = hashed_password.decode('utf-8')

        cursor.execute(
            query,
            (passageiro.nome, passageiro.sobrenome,
            passageiro.nome_usuario,
            senha, passageiro.telefone)
        )

        db.conexao.commit()
        
        cursor.close()

        return {
            "status": "sucesso",
            "content": passageiro.model_dump_json()
        }
    
    except Error as e:
        db.conexao.rollback()

        return {
            "status": "erro",
            "erro": e
        }

@router.post("/login")
def fazer_login(login: LoginSchema):
    query = """
            SELECT nome, nome_usuario, senha FROM passageiros WHERE nome_usuario = %s; 
            """

    try:
        cursor = db.conexao.cursor()

        cursor.execute(query, (login.nome_usuario,))

        dados = cursor.fetchone()

        if dados is None:
            return {
                "status": "erro",
                "mensagem": "Usuário não encontrado."
            }

        tempo = datetime.now() + timedelta(minutes=30)

        payload = {
            "nome": dados[0],
            "nome_usuario": dados[1],
            "exp": int(tempo.timestamp())
        }

        if verifica_senha(login.senha, dados[2]):
            encoded = jwt.encode(
                payload=payload,
                key=os.getenv("SECRET_KEY"),
                algorithm=str(os.getenv("ALGORITHM"))
                )

            return {    
                "status": "sucesso",
                "mensagem": "Você está totalmente conectado(a)",
                "token": encoded

            }
        
        else:
            return {
                "status": "erro",
                "erro": "Usuário ou senha incorretos."
            }
        
    except Error as e:
        return {
            "status": "erro",
            "erro": str(e)
        }

@router.get("/")
def get_passageiros():
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