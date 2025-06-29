from Veterinaria.database import get_session
from repositories.mascota_repository import MascotaRepository


def crear_mascota(**data):
    with get_session() as db:
        repo = MascotaRepository(db)
        return repo.add(**data)


def listar_mascotas():
    with get_session() as db:
        repo = MascotaRepository(db)
        return repo.get_all()
