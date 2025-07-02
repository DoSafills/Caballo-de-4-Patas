from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import HistorialCreate
import models
from datetime import date

router = APIRouter(prefix="/historial", tags=["historial"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{id_mascota}")
def obtener_historial(id_mascota: int, db: Session = Depends(get_db)):
    historial = db.query(models.HistorialMedico).filter_by(id_mascota=id_mascota).all()
    if not historial:
        raise HTTPException(status_code=404, detail="No se encontró historial para esta mascota")
    return historial

@router.post("/")
def registrar_historial(datos: HistorialCreate, db: Session = Depends(get_db)):
    nuevo = models.HistorialMedico(
        fecha=date.today(),
        descripcion=datos.descripcion,
        id_mascota=datos.id_mascota
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
