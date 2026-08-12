import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def postgres_conn():
    conn = psycopg2.connect(
        host="localhost",
        dbname="Crypto_Analytics",
        user="postgres",
        password = os.getenv("DB_Password"),
        port=5432
    )

    return conn
