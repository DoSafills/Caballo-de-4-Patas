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

    CAMPOS_COMUNES = ["rut", "nombre", "apellido", "edad", "email"]
    CAMPOS_ESPECIFICOS = {
        "admin": ["contrasena"],
        "veterinario": ["contrasena", "especializacion"],
        "recepcionista": ["contrasena"],
        "cliente": [],  # puede expandirse si cliente tiene más
    }

    def __init__(self, session: Session, tipo: str):
        self.session = session
        self.tipo = tipo
        self.model = self.MODELOS[tipo]
        self.repo = BaseRepository(session, self.model)

    def crear(self, **data):
        # Verifica si ya existe un usuario con ese RUT
        rut = data.get("rut")
        if self.repo.get(rut=rut):
            return None

        # Separar los campos comunes (Persona) y específicos (Admin, etc.)
        comunes = {campo: data[campo] for campo in self.CAMPOS_COMUNES if campo in data}
        especificos = {campo: data[campo] for campo in self.CAMPOS_ESPECIFICOS[self.tipo] if campo in data}

        # Combinar para instanciar la subclase
        instancia = self.model(**comunes, **especificos)

        self.session.add(instancia)
        self.session.commit()
        return instancia

    def obtener(self, **filters):
        return self.repo.get(**filters)

    def todos(self):
        return self.repo.get_all()

    def actualizar(self, obj, **data):
        return self.repo.update(obj, **data)

    def eliminar(self, obj):
        self.repo.delete(obj)
