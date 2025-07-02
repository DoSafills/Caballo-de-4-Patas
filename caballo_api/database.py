
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import create_tables

DATABASE_URL = "sqlite:///veterinaria.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def inicializar_base():
    create_tables(engine)
