from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from Veterinaria.models import create_tables

DATABASE_URL = "sqlite:///Veterinaria/veterinaria.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para inicializar tablas (si la usas desde un script)
def inicializar_base():
    create_tables(engine)

# Función para usar desde servicios, sin pasar SessionLocal manualmente
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()