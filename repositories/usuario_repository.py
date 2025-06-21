from sqlalchemy.orm import Session
from models import Admin, Veterinario, Recepcionista, Cliente
from .base_repository import BaseRepository


class UsuarioRepository:
    """Repositorio especializado para entidades de usuario."""

    MODELOS = {
        "admin": Admin,
        "veterinario": Veterinario,
        "recepcionista": Recepcionista,
        "cliente": Cliente,
    }

    def __init__(self, session: Session, tipo: str):
        model = self.MODELOS[tipo]
        self.repo = BaseRepository(session, model)

    def crear(self, **data):
        return self.repo.add(**data)

    def obtener(self, **filters):
        return self.repo.get(**filters)

    def todos(self):
        return self.repo.get_all()

    def actualizar(self, obj, **data):
        return self.repo.update(obj, **data)

    def eliminar(self, obj):
        self.repo.delete(obj)
