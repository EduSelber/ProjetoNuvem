from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import psycopg2
import os
import time
# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém as variáveis de ambiente
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
DATABASE_URL_ROOT = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/postgres"
# Função para criar o banco de dados se ele não existir
def create_database():
    # Conecta ao PostgreSQL sem o SQLAlchemy para evitar transações
    conn = psycopg2.connect(DATABASE_URL_ROOT)
    conn.autocommit = True  # Configura autocommit para evitar o uso de transações.
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {POSTGRES_DB}")
    except psycopg2.errors.DuplicateDatabase:
        print(f"O banco de dados '{POSTGRES_DB}' já existe.")
    finally:
        conn.close()

# Tenta conectar ao banco de dados; cria-o se falhar
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    engine.connect()
except OperationalError:
    create_database()
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
