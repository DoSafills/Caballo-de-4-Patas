import logging
from sqlalchemy.orm import Session
from models import Admin, Cliente, Consulta, Mascota, Persona, Recepcionista, Veterinario
from factoriUsuario import FactoriUsuario
"""Funciones CRUD para las entidades principales."""
from datetime import datetime
from database import get_session
from repositories.usuario_repository import UsuarioRepository
from repositories.mascota_repository import MascotaRepository
from repositories.consulta_repository import ConsultaRepository

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

# --------------------------- Usuarios ---------------------------
def crear_usuario(tipo: str, datos: dict):
    """Crea un usuario del tipo indicado."""
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.crear(**datos)

def obtener_usuario(tipo: str, rut: str):
    """Obtiene un usuario por RUT."""
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.obtener(rut=rut)

def actualizar_usuario(tipo: str, rut: str, datos: dict):
    """Actualiza un usuario existente."""
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        usuario = repo.obtener(rut=rut)
        if usuario:
            return repo.actualizar(usuario, **datos)
        return None

def eliminar_usuario(tipo: str, rut: str) -> bool:
    """Elimina un usuario y devuelve True si existía."""
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        usuario = repo.obtener(rut=rut)
        if usuario:
            db.delete(usuario)
            # Intentamos eliminar persona relacionada en la misma transacción
            persona = db.query(Persona).filter_by(rut=rut).first()
            if persona:
                db.delete(persona)
            db.commit()
            repo.eliminar(usuario)
            return True
        return False

def listar_usuarios(tipo: str):
    """Lista todos los usuarios del tipo dado."""
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.todos()

# --------------------------- Mascotas ---------------------------
def crear_mascota(datos: dict):
    with get_session() as db:
        repo = MascotaRepository(db)
        return repo.add(**datos)

def obtener_mascota(id_mascota: int):
    with get_session() as db:
        repo = MascotaRepository(db)
        return repo.get(id_mascota=id_mascota)

def actualizar_mascota(id_mascota: int, datos: dict):
    with get_session() as db:
        repo = MascotaRepository(db)
        mascota = repo.get(id_mascota=id_mascota)
        if mascota:
            return repo.update(mascota, **datos)
        return None

def eliminar_mascota(id_mascota: int) -> bool:
    with get_session() as db:
        repo = MascotaRepository(db)
        mascota = repo.get(id_mascota=id_mascota)
        if mascota:
            db.delete(mascota)
            db.commit()
            repo.delete(mascota)
            return True
        return False

# --------------------------- Consultas ---------------------------
def crear_consulta(
    fecha_hora: datetime,
    id_recepcionista: int,
    id_mascota: int,
    id_vet: int,
    id_cliente: int,
    motivo: str,
):
    with get_session() as db:
        repo = ConsultaRepository(db)
        return repo.add(
            fecha_hora=fecha_hora,
            id_recepcionista=id_recepcionista,
            id_mascota=id_mascota,
            id_vet=id_vet,
            id_cliente=id_cliente,
            motivo=motivo
        )

def obtener_consulta(id_consulta: int):
    with get_session() as db:
        repo = ConsultaRepository(db)
        return repo.get(id_consulta=id_consulta)

def actualizar_consulta(id_consulta: int, datos: dict):
    with get_session() as db:
        repo = ConsultaRepository(db)
        consulta = repo.get(id_consulta=id_consulta)
        if consulta:
            return repo.update(consulta, **datos)
        return None

def eliminar_consulta(id_consulta: int) -> bool:
    with get_session() as db:
        repo = ConsultaRepository(db)
        consulta = repo.get(id_consulta=id_consulta)
        if consulta:
            db.delete(consulta)
            db.commit()
            repo.delete(consulta)
            return True
        return False

def listar_mascotas():
    with get_session() as db:
        repo = MascotaRepository(db)
        return repo.get_all()

def listar_consultas():
    with get_session() as db:
        repo = ConsultaRepository(db)
        return repo.get_all()
