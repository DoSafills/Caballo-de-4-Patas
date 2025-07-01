from database import get_session
from repositories.mascota_repository import MascotaRepository
from models import Mascota
from schemas import MascotaCreate, MascotaUpdate

from fastapi import HTTPException

def crear_mascota(mascota: MascotaCreate):
    with get_session() as db:
        repo = MascotaRepository(db)
        return repo.add(**mascota.dict())

def obtener_mascotas() -> list[Mascota]:
    with next(get_session()) as db:
        repo = MascotaRepository(db)
        return repo.get_all()

def actualizar_mascota(id_mascota: int, datos: MascotaUpdate) -> Mascota:
    with next(get_session()) as db:
        repo = MascotaRepository(db)
        mascota = repo.get_by_id(id_mascota)
        if not mascota:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")

        data_actualizada = {
            k: v for k, v in datos.dict().items() if v is not None
        }
        return repo.update(mascota, **data_actualizada)