import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Alterar quando sair a fase de testes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sicherplan.db")

SQLALCHEMY_DATABASE_URL = "sqlite:///./sicherplan.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Apos a virgula pode ser removido se nao for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Abre e fecha a conexão com o banco em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()