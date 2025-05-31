from sqlalchemy.orm import Session
from models import Admin, Cliente, Consulta, Mascota, Persona, Recepcionista, Veterinario
import models
from models import Cita
from datetime import datetime

MODELOS = {
    "admin": Admin,
    "cliente": Cliente,
    "mascota": Mascota,
    "recepcionista": Recepcionista,
    "veterinario": Veterinario
}

# CRUD adminapp
def obtener_usuarios_por_tipo(db: Session, tipo: str):
    if tipo == "todos":
        resultado = []
        for modelo in MODELOS.values():
            resultado.extend(db.query(modelo).all())
        return resultado
    modelo = MODELOS.get(tipo)
    return db.query(modelo).all() if modelo else []

def eliminar_usuario(db: Session, rut: str, tipo: str):
    modelo = MODELOS.get(tipo)
    if not modelo:
        return False
    usuario = db.query(modelo).filter_by(rut=rut).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return True
    return False

def actualizar_usuario(db: Session, rut: str, tipo: str, nuevos_datos: dict):
    modelo = MODELOS.get(tipo)
    if not modelo:
        return None
    usuario = db.query(modelo).filter_by(rut=rut).first()
    if usuario:
        for k, v in nuevos_datos.items():
            setattr(usuario, k, v)
        db.commit()
        db.refresh(usuario)
        return usuario
    return None

def crear_usuario(db, tipo, datos):
    try:
        if tipo == "admin":
            usuario = Admin(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                tipo="admin",
                contrasena=datos["contrasena"]
            )
        elif tipo == "recepcionista":
            usuario = Recepcionista(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                tipo="recepcionista",
                contrasena=datos["contrasena"]
            )
        elif tipo == "veterinario":
            usuario = Veterinario(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                tipo="veterinario",
                contrasena=datos["contrasena"],
                especializacion=datos["especializacion"]
            )
        else:
            return False

        db.add(usuario)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"error al crear usuario: {e}")
        return False

def obtener_admin_por_rut(db, rut):
    return db.query(Admin).filter_by(rut=rut).first()

def obtener_veterinario_por_rut(db, rut):
    return db.query(Veterinario).filter_by(rut=rut).first()

def obtener_recepcionista_por_rut(db, rut):
    return db.query(Recepcionista).filter_by(rut=rut).first()


def crear_mascota(db, mascota_data):
    try:
        nueva_mascota = models.Mascota(**mascota_data)
        db.add(nueva_mascota)
        db.commit()
        db.refresh(nueva_mascota)
        return nueva_mascota
    except Exception as e:
        db.rollback()
        raise e
    

def crear_cita(db: Session, id_cliente: int, id_mascota: int, fecha_hora: datetime):
    nueva_cita = Cita(
        id_cliente=id_cliente,
        id_mascota=id_mascota,
        fecha_hora=fecha_hora
    )
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

def obtener_citas(db: Session):
    return db.query(Cita).all()

def obtener_citas_por_cliente(db: Session, id_cliente: int):
    return db.query(Cita).filter(Cita.id_cliente == id_cliente).all()

def eliminar_cita(db: Session, id_cita: int):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if cita:
        db.delete(cita)
        db.commit()
        return True
    return False

def actualizar_cita(db: Session, id_cita: int, nuevos_datos: dict):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()
    if cita:
        for k, v in nuevos_datos.items():
            setattr(cita, k, v)
        db.commit()
        db.refresh(cita)
        return cita
    return None
