from sqlalchemy.orm import Session
from Veterinaria.models import Mascota
from Veterinaria.schemas import MascotaCreate
from Veterinaria.schemas import MascotaUpdate
from fastapi import HTTPException

def crear_mascota(db: Session, datos: MascotaCreate):
    mascota = Mascota(**datos.dict())
    db.add(mascota)
    db.commit()
    db.refresh(mascota)
    return mascota

def obtener_mascotas(db: Session):
    return db.query(Mascota).all()

def actualizar_mascota(db: Session, id_mascota: int, datos: MascotaUpdate) -> Mascota:
    mascota = db.query(Mascota).filter(Mascota.id_mascota == id_mascota).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    # Solo actualiza los campos que no son None
    if datos.edad is not None:
        mascota.edad = datos.edad
    if datos.sexo is not None:
        mascota.sexo = datos.sexo
    if datos.estado is not None:
        mascota.estado = datos.estado

    db.commit()
    db.refresh(mascota)
    return mascota