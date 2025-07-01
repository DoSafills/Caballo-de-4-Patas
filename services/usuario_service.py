from database import get_session
from repositories.usuario_repository import UsuarioRepository
from models import Admin, Recepcionista, Veterinario, Cliente

def crear_usuario(tipo: str, datos: dict):
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.crear(**datos)

def listar_usuarios(tipo: str = "cliente"):
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.todos()

def eliminar_usuario(rut: str):
    with get_session() as db:
        for modelo in [Admin, Recepcionista, Veterinario, Cliente]:
            usuario = db.query(modelo).filter_by(rut=rut).first()
            if usuario:
                db.delete(usuario)
                db.commit()
                return True
        return False
    
def actualizar_usuario(tipo: str, rut: str, nuevos_datos: dict):
    with get_session() as db:
        modelo = {
            "admin": Admin,
            "recepcionista": Recepcionista,
            "veterinario": Veterinario,
            "cliente": Cliente
        }.get(tipo)

        if not modelo:
            return False

        usuario = db.query(modelo).filter_by(rut=rut).first()
        if not usuario:
            return False

        for clave, valor in nuevos_datos.items():
            setattr(usuario, clave, valor)

        db.commit()
        return True