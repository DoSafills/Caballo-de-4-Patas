from database import get_session
from repositories.usuario_repository import UsuarioRepository


def crear_usuario(tipo: str, datos: dict):
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.crear(**datos)


def listar_usuarios(tipo: str = "cliente"):
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.todos()

def eliminar_usuario(tipo: str, rut: str):
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        usuario = repo.obtener(rut=rut)
        if usuario:
            repo.eliminar(usuario)
            db.commit()
            return True
        return False

def actualizar_usuario(tipo: str, rut: str, nuevos_datos: dict):
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        usuario = repo.obtener(rut=rut)
        if usuario:
            repo.actualizar(usuario, **nuevos_datos)
            db.commit()
            return True
        return False
