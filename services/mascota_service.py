from database import get_session
from repositories.mascota_repository import MascotaRepository
from models import Mascota


def crear_mascota(**data):
    with get_session() as db:
        repo = MascotaRepository(db)
        return repo.add(**data)


def listar_mascotas():
    with get_session() as db:
        repo = MascotaRepository(db)
        return repo.get_all()

def registrar_mascota(data: dict):
    with get_session() as db:
        try:
            mascota = Mascota(**data)
            db.add(mascota)
            db.commit()
            return True
        except Exception as e:
            print("Error al registrar mascota:", e)
            return False
        
def obtener_mascotas():
    with get_session() as db:
        return db.query(Mascota).all()

def actualizar_mascota(id_mascota, nuevos_datos: dict):
    with get_session() as db:
        mascota = db.query(Mascota).get(id_mascota)
        if mascota:
            for k, v in nuevos_datos.items():
                setattr(mascota, k, v)
            db.commit()
            return True
        return False