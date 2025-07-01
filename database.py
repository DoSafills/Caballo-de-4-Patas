from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import create_tables
from contextlib import contextmanager 

DATABASE_URL = "sqlite:///veterinaria.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para inicializar tablas
def inicializar_base():
    create_tables(engine)

# Función para usar desde servicios, sin pasar SessionLocal manualmente
@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()