from sqlalchemy.orm import Session
from veterinaria2.models import Mascota
from veterinaria2.schemas import MascotaCreate

def crear_mascota(db: Session, datos: MascotaCreate):
    mascota = Mascota(**datos.dict())
    db.add(mascota)
    db.commit()
    db.refresh(mascota)
    return mascota

def obtener_mascotas(db: Session):
    return db.query(Mascota).all()