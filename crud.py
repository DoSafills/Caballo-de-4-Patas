from sqlalchemy.orm import Session
from models import Admin, Cliente, Consulta, Mascota, Persona, Recepcionista, Veterinario
from factoriUsuario import FactoriUsuario
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

        persona = db.query(Persona).filter_by(rut=rut).first()
        if persona:
            db.delete(persona)
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
        usuario = FactoriUsuario.crear_usuario(tipo, datos)
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

def crear_mascota(db, nombre, id_cliente, especie, raza, edad):
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

def obtener_mascota_por_nombre(db, nombre):
    return db.query(Mascota).filter(Mascota.nombre == nombre).first()

def crear_consulta(db, fecha_hora: datetime, id_recepcionista: int, id_mascota: int, id_vet: int, id_cliente: int, motivo: str):
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

def eliminar_mascota(db, mascota_id):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if mascota:
        db.delete(mascota)
        db.commit()
        return True
    return False

def actualizar_mascota(db, chapa, nombre, edad, peso, altura):
    mascota = db.query(Mascota).filter(Mascota.id == chapa).first()
    if mascota:
        mascota.nombre = nombre
        mascota.edad = edad
        mascota.peso = peso
        mascota.altura = altura
        db.commit()
        db.refresh(mascota)
        return mascota
    return None

def obtener_mascotas_por_id(db, mascota_id):
    return db.query(Mascota).filter(Mascota.id == mascota_id).first()


def eliminar_consulta(db, consulta_id: int):
    consulta = db.query(Consulta).filter(Consulta.id_consulta == consulta_id).first()
    if consulta:
        db.delete(consulta)
        db.commit()
        return True
    return False

def actualizar_consulta(db, consulta_id: int, nuevos_datos: dict):
    consulta = db.query(Consulta).filter(Consulta.id_consulta == consulta_id).first()
    if consulta:
        for key, value in nuevos_datos.items():
            setattr(consulta, key, value)
        db.commit()
        db.refresh(consulta)
        return consulta
    return None


def obtener_cliente_por_rut(db, rut):
    return db.query(Cliente).filter(Cliente.rut == rut).first()

def crear_cliente(db, rut, nombre="", apellido="", edad=None, email=""):
    try:
        nuevo_cliente = Cliente(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            email=email,
            tipo="cliente"  
        )
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente
    except Exception as e:
        db.rollback()
        print(f"Error al crear cliente: {e}")
        return None
    
def obtener_admin_por_rut(db, rut):
    return db.query(Admin).filter_by(rut=rut).first()

def obtener_veterinario_por_rut(db, rut):
    return db.query(Veterinario).filter_by(rut=rut).first()

def obtener_recepcionista_por_rut(db, rut):
    return db.query(Recepcionista).filter_by(rut=rut).first()