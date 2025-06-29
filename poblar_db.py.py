#ex main



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Asegúrate que esto importa la clase Base
import models  # Esto debe importar también la clase Mascota
from sqlalchemy.orm import Session
from database import SessionLocal, inicializar_base
import crud
from datetime import datetime

# Inicializar base de datos y sesión
inicializar_base()
db: Session = SessionLocal()

engine = create_engine("sqlite:///veterinaria.db")
Base.metadata.create_all(engine)

# Crear un cliente
cliente_data = {
    "rut": "12345678-9",
    "nombre": "Camila",
    "apellido": "López",
    "edad": 30,
    "email": "camila@example.com",
    "tipo": "cliente",
    "id_cliente": 1,
    "id_mascota": None
}
cliente = crud.crear_cliente(db, cliente_data)

# Crear un veterinario
veterinario_data = {
    "rut": "11223344-5",
    "nombre": "Dr. Ramírez",
    "apellido": "Pérez",
    "edad": 45,
    "email": "dr.ramirez@example.com",
    "tipo": "veterinario",
    "id_vet": 1,
    "especializacion": "Cirugía",
    "contrasena": "segura123"
}
veterinario = crud.crear_veterinario(db, veterinario_data)

# Crear una mascota
mascota_data = {
    "nombre": "Luna",
    "raza": "Golden Retriever",
    "sexo": "Hembra",
    "dieta": "Especial",
    "caracter": "Activa",
    "habitat": "Casa",
    "id_vet": veterinario.id_vet,
    "edad": 5,
    "peso": "30kg",
    "altura": "60cm"
}
mascota = crud.crear_mascota(db, mascota_data)

# Asignar mascota al cliente
crud.actualizar_cliente(db, cliente.id_cliente, {"id_mascota": mascota.id_mascota})

# Crear un recepcionista
recepcionista_data = {
    "rut": "55667788-0",
    "nombre": "Andrés",
    "apellido": "Martínez",
    "edad": 28,
    "email": "andres@example.com",
    "tipo": "recepcionista",
    "id_recepcionista": 1,
    "contrasena": "clave123"
}
recepcionista = crud.crear_recepcionista(db, recepcionista_data)

# Crear una consulta
consulta_data = {
    "fecha_hora": datetime.now(),
    "id_recepcionista": recepcionista.id_recepcionista,
    "id_mascota": mascota.id_mascota,
    "id_vet": veterinario.id_vet,
    "id_cliente": cliente.id_cliente,
    "motivo": "Revisión anual"
}
consulta = crud.crear_consulta(db, consulta_data)

# Crear un cliente
admin_data = {
    "rut": "22334455-6",
    "nombre": "Pepe",
    "apellido": "Tapia",
    "edad": 30,
    "email": "ptapia@example.com",
    "tipo": "admin",
    "id_admin": 1,
    "contrasena": "clave123"
}
admin = crud.crear_admin(db, admin_data)


print(f"Consulta creada para {mascota.nombre} con el Dr. {veterinario.nombre} registrada por {recepcionista.nombre}")
print("Tablas creadas correctamente")