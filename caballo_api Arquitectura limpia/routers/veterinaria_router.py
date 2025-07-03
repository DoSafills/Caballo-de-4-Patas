from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.veterinaria_service import registrar_mascota_service, obtener_mascotas_service, obtener_mascotas_por_cliente
from entities.schemas import MascotaCreate, MascotaOut, MascotaUpdate
import models.models as models
from models.models import Mascota
router = APIRouter(prefix="/veterinaria", tags=["veterinaria"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/registrar", response_model=MascotaOut)
def registrar_mascota(datos: MascotaCreate, db: Session = Depends(get_db)):
    mascota = registrar_mascota_service(db, datos.dict())
    return mascota

@router.get("/mascotas", response_model=list[MascotaOut])
def listar_mascotas(db: Session = Depends(get_db)):
    return obtener_mascotas_service(db)

@router.get("/mascotas/cliente/{id_cliente}", response_model=list[MascotaOut])
def listar_mascotas_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return obtener_mascotas_por_cliente(db, id_cliente)

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

@router.get("/mascotas/nombre/{nombre}", response_model=MascotaOut)
def obtener_mascota_por_nombre(nombre: str, db: Session = Depends(get_db)):
    mascota = db.query(Mascota).filter(Mascota.nombre == nombre).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

