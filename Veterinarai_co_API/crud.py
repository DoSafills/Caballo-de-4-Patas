import logging
from sqlalchemy.orm import Session
from models import Admin, Cliente, Consulta, Mascota, Persona, Recepcionista, Veterinario
from factoriUsuario import FactoriUsuario
from datetime import datetime
import models

logger = logging.getLogger(__name__)

MODELOS = {
    "admin": Admin,
    "cliente": Cliente,
    "mascota": Mascota,
    "recepcionista": Recepcionista,
    "veterinario": Veterinario
}


# --- CRUD de usuarios ---
def obtener_usuarios_por_tipo(db: Session, tipo: str):
    if tipo == "todos":
        resultado = []
        for modelo in MODELOS.values():
            resultado.extend(db.query(modelo).all())
        return resultado
    modelo = MODELOS.get(tipo)
    return db.query(modelo).all() if modelo else []

def crear_usuario(db: Session, tipo: str, datos: dict):
    try:
        usuario = FactoriUsuario.crear_usuario(tipo, datos)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        return None

def actualizar_usuario(db: Session, rut: str, tipo: str, nuevos_datos: dict):
    modelo = MODELOS.get(tipo)
    if not modelo:
        return None
    usuario = db.query(modelo).filter_by(rut=rut).first()
    if usuario:
        try:
            for k, v in nuevos_datos.items():
                setattr(usuario, k, v)
            db.commit()
            db.refresh(usuario)
            return usuario
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar usuario {rut}: {e}")
            return None
    return None

def eliminar_usuario(db: Session, rut: str, tipo: str):
    modelo = MODELOS.get(tipo)
    if not modelo:
        return False
    try:
        usuario = db.query(modelo).filter_by(rut=rut).first()
        if usuario:
            db.delete(usuario)
            # Intentamos eliminar persona relacionada en la misma transacción
            persona = db.query(Persona).filter_by(rut=rut).first()
            if persona:
                db.delete(persona)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar usuario {rut}: {e}")
        return False
    
def crear_veterinario(db: Session, data: dict):
    nuevo = models.Veterinario(**data)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# --- Métodos específicos por tipo de usuario ---
def obtener_admin_por_rut(db: Session, rut: str):
    return db.query(Admin).filter_by(rut=rut).first()

def obtener_veterinario_por_rut(db: Session, rut: str):
    return db.query(Veterinario).filter_by(rut=rut).first()

def obtener_recepcionista_por_rut(db: Session, rut: str):
    return db.query(Recepcionista).filter_by(rut=rut).first()

def obtener_cliente_por_rut(db: Session, rut: str):
    return db.query(Cliente).filter(Cliente.rut == rut).first()

def crear_cliente(db: Session, rut: str, nombre="", apellido="", edad=None, email="", rut_vet_preferido=""):
    try:
        nuevo_cliente = Cliente(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            email=email,
            rut_vet_preferido=rut_vet_preferido,
            
            tipo="cliente"
        )
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear cliente: {e}")
        return None

# --- CRUD de Mascotas ---
def crear_mascota(db: Session, nombre, id_cliente, especie, raza, edad):
    try:
        nueva_mascota = Mascota(
            nombre=nombre,
            id_cliente=id_cliente,
            especie=especie,
            raza=raza,
            edad=edad
        )
        db.add(nueva_mascota)
        db.commit()
        db.refresh(nueva_mascota)
        return nueva_mascota
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear mascota: {e}")
        return None

def obtener_mascota_por_nombre(db: Session, nombre: str):
    return db.query(Mascota).filter(Mascota.nombre == nombre).first()

def obtener_mascotas_por_id(db: Session, mascota_id: int):
    return db.query(Mascota).filter(Mascota.id == mascota_id).first()

def actualizar_mascota(db: Session, chapa: int, nombre: str, edad: int, peso: float, altura: float):
    mascota = db.query(Mascota).filter(Mascota.id == chapa).first()
    if mascota:
        try:
            mascota.nombre = nombre
            mascota.edad = edad
            mascota.peso = peso
            mascota.altura = altura
            db.commit()
            db.refresh(mascota)
            return mascota
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar mascota {chapa}: {e}")
            return None
    return None

def eliminar_mascota(db: Session, mascota_id: int):
    try:
        mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
        if mascota:
            db.delete(mascota)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar mascota {mascota_id}: {e}")
        return False

# --- CRUD de Consultas ---
def crear_consulta(db: Session, fecha_hora: datetime, id_recepcionista: int, id_mascota: int, id_vet: int, id_cliente: int, motivo: str):
    try:
        consulta = Consulta(
            fecha_hora=fecha_hora,
            id_recepcionista=id_recepcionista,
            id_mascota=id_mascota,
            id_vet=id_vet,
            id_cliente=id_cliente,
            motivo=motivo
        )
        db.add(consulta)
        db.commit()
        db.refresh(consulta)
        return consulta
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear consulta: {e}")
        return None

def eliminar_consulta(db: Session, consulta_id: int):
    try:
        consulta = db.query(Consulta).filter(Consulta.id_consulta == consulta_id).first()
        if consulta:
            db.delete(consulta)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar consulta {consulta_id}: {e}")
        return False

def actualizar_consulta(db: Session, consulta_id: int, nuevos_datos: dict):
    consulta = db.query(Consulta).filter(Consulta.id_consulta == consulta_id).first()
    if consulta:
        try:
            for key, value in nuevos_datos.items():
                setattr(consulta, key, value)
            db.commit()
            db.refresh(consulta)
            return consulta
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar consulta {consulta_id}: {e}")
            return None
    return None

def obtener_todos_los_clientes(db: Session):
    return db.query(Cliente).all()

def obtener_mascotas_de_cliente(db: Session, id_cliente: int):
    return db.query(Mascota).filter(Mascota.id_cliente == id_cliente).all()

def actualizar_estado_mascota(db: Session, id_mascota: int, nuevo_estado: str):
    mascota = db.query(Mascota).filter(Mascota.id == id_mascota).first()
    if not mascota:
        return None
    try:
        mascota.estado = nuevo_estado
        db.commit()
        db.refresh(mascota)
        return mascota
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar estado de mascota {id_mascota}: {e}")
        return None
