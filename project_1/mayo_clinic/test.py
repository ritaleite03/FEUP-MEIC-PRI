import psycopg2
from psycopg2 import sql
import os
import traceback

def connect_to_db():
    try:

        conn = psycopg2.connect("dbname=postgres_db user=postgres password=p.postgres host=postgres port=5432").set_client_encoding('Latin1')
        
        # Criando um cursor para executar comandos
        cursor = conn.cursor()

        # Executando uma consulta simples
        cursor.execute("SELECT * FROM diseases;")
        records = cursor.fetchall()

        # Exibindo os resultados
        for record in records:
            print(record)

        # Fechando a conexão
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


if __name__ == "__main__":
    connect_to_db()
