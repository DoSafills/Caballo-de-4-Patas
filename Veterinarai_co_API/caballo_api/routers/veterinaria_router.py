# routers/veterinaria_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import MascotaCreate, MascotaOut
import models
from schemas import MascotaUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registrar", response_model=MascotaOut)
def registrar_mascota(datos: MascotaCreate, db: Session = Depends(get_db)):
    nueva = models.Mascota(**datos.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/mascotas", response_model=list[MascotaOut])
def obtener_mascotas(db: Session = Depends(get_db)):
    return db.query(models.Mascota).all()

@router.get("/mascotas/{id_mascota}", response_model=MascotaOut)
def obtener_mascota(id_mascota: int, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota).filter_by(id_mascota=id_mascota).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota



@router.put("/mascotas/{id_mascota}", response_model=MascotaOut)
def actualizar_mascota(id_mascota: int, datos: MascotaUpdate, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota).filter_by(id_mascota=id_mascota).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(mascota, key, value)

    db.commit()
    db.refresh(mascota)
    return mascota

