from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Configuración de la base de datos local
DATABASE_URL = "sqlite:///local_database.db"  # Cambia esto si usas PostgreSQL o MySQL

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inicializar la base de datos (crear tablas)
def init_db():
    # Crear las tablas en la base de datos si no existen
    Base.metadata.create_all(bind=engine)

# Crear una instancia de sesión para interactuar con la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db  # Se usa para obtener la sesión cuando sea necesario
    finally:
        db.close()  # Se asegura de cerrar la sesión después de usarla
