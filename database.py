from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from models import create_tables

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///veterinaria.db")


class DatabaseSingleton:
    """Singleton para la conexión a la base de datos."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(DATABASE_URL, echo=False)
            cls._instance.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=cls._instance.engine
            )
            create_tables(cls._instance.engine)
        return cls._instance


def get_session():
    """Obtiene una nueva sesión de base de datos."""
    return DatabaseSingleton().SessionLocal()


# Objetos para compatibilidad con el código existente
engine = DatabaseSingleton().engine
SessionLocal = DatabaseSingleton().SessionLocal


def inicializar_base():
    """Crea las tablas si no existen."""
    create_tables(engine)
