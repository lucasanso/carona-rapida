from psycopg2 import connect, Error
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class PostgresConnect:
    def __init__(self):
        print("Conectando ao banco PostgreSQL")
        self.connecting()
        self.init_database()

    def connecting(self):
        try:
            self.conexao = connect(
                user = os.getenv("POSTGRES_USER"),
                password = os.getenv("POSTGRES_PASS"),
                database=os.getenv("POSTGRES_DB"),
                host="localhost"
            )

            print("[SUCESSO] Conexão realizada com sucesso")

        except Error as e:
            print(f"Erro ao conectar no PostgreSQL: {e}")
    
    def init_database(self):
        with open("init.sql", "r") as file:
            query = file.read()

            cursor = self.conexao.cursor()

            try:
                cursor.execute(query)
                
                self.conexao.commit()
                print("Tabelas inicializadas com sucesso no banco de dados")

            except Error as e:
                print(f"Ocorreu um erro ao inicializar as tabelas: {e}")

                self.conexao.rollback()
                
        self.conexao.close()

if __name__ == "__main__":
    teste = PostgresConnect()