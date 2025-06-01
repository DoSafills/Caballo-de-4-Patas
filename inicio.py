from sqlalchemy.orm import Session
from database import SessionLocal, inicializar_base
import crud


# Inicializar base de datos y sesión
inicializar_base()
db: Session = SessionLocal()

# Crear un cliente

admin_data = {
    "rut": "admin",
    "nombre": "admin",
    "apellido": "admin",
    "edad": 0,
    "email": "adminadmin",
    "tipo": "admin",
    "id_admin": 1,
    "contrasena": "admin"
}
crud.crear_usuario(db, "admin", admin_data)