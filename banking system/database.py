import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():

    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="banking_db",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )

    return connection