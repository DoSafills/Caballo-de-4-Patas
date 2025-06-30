from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Veterinaria.models import create_tables
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///Veterinaria/veterinaria.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def inicializar_base():
    create_tables(engine)
