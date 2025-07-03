
from sqlalchemy.orm import Session
from methods.factoriUsuario import FactoriUsuario
import logging
from models.models import Admin, Recepcionista, Veterinario, Persona

logger = logging.getLogger(__name__)


MODELOS = {
    "admin": Admin,
    "recepcionista": Recepcionista,
    "veterinario": Veterinario
}

def obtener_modelo_por_tipo(tipo: str):
    return MODELOS.get(tipo)

def crear_usuario_service(db: Session, datos):
    try:
        usuario = FactoriUsuario.crear_usuario(datos.tipo, datos.dict())
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear usuario: {e}")
        return None


def actualizar_usuario_service(db: Session, tipo: str, rut: str, nuevos_datos):
    modelo = obtener_modelo_por_tipo(tipo)
    if not modelo:
        return None
    usuario = db.query(modelo).filter_by(rut=rut).first()
    if usuario:
        try:
            for campo, valor in nuevos_datos.dict(exclude_unset=True).items():
                setattr(usuario, campo, valor)
            db.commit()
            db.refresh(usuario)
            return usuario
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar usuario {rut}: {e}")
    return None


def eliminar_usuario_service(db: Session, tipo: str, rut: str):
    modelo = obtener_modelo_por_tipo(tipo)
    if not modelo:
        return False
    usuario = db.query(modelo).filter_by(rut=rut).first()
    if usuario:
        try:
            db.delete(usuario)
            # Eliminar también de persona si aplica
            persona = db.query(Persona).filter_by(rut=rut).first()
            if persona:
                db.delete(persona)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar usuario {rut}: {e}")
    return False

