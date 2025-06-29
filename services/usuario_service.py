from veterinaria2.database import get_session
from repositories.usuario_repository import UsuarioRepository


def crear_usuario(tipo: str, datos: dict):
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.crear(**datos)


def listar_usuarios(tipo: str = "cliente"):
    with get_session() as db:
        repo = UsuarioRepository(db, tipo)
        return repo.todos()
