from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.veterinaria_service import registrar_mascota_service, obtener_mascotas_service, obtener_mascotas_por_cliente
from schemas import MascotaCreate, MascotaOut

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
