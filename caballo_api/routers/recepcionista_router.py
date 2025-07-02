from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from caballo_api.database import get_db
from caballo_api import models
from caballo_api.schemas import UsuarioBase, MascotaCreate
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/recepcionista", tags=["Recepcionista"])

# ============================
# CLIENTES
# ============================

@router.post("/clientes/", response_model=dict)
def crear_cliente(cliente: UsuarioBase, db: Session = Depends(get_db)):
    db_persona = db.query(models.Persona).filter_by(rut=cliente.rut).first()
    if db_persona:
        raise HTTPException(status_code=400, detail="El cliente ya existe")

    nueva_persona = models.Cliente(
        rut=cliente.rut,
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        edad=cliente.edad,
        email=cliente.email
    )
    db.add(nueva_persona)
    db.commit()
    return {"mensaje": "Cliente creado con éxito"}


@router.get("/clientes/{rut}", response_model=dict)
def obtener_cliente_por_rut(rut: str, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter_by(rut=rut).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {
        "id": cliente.id_cliente,
        "nombre": cliente.nombre,
        "apellido": cliente.apellido,
        "email": cliente.email
    }

# ============================
# CONSULTAS
# ============================

class ConsultaCreate(BaseModel):
    id_cliente: int
    id_mascota: int
    id_vet: int
    id_recepcionista: int
    fecha_hora: datetime
    motivo: str

class ConsultaUpdate(BaseModel):
    id_cliente: Optional[int]
    id_mascota: Optional[int]
    id_vet: Optional[int]
    id_recepcionista: Optional[int]
    fecha_hora: Optional[datetime]
    motivo: Optional[str]

@router.post("/consultas/", response_model=dict)
def crear_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    nueva = models.Consulta(**consulta.dict())
    db.add(nueva)
    db.commit()
    return {"mensaje": "Consulta creada"}

@router.get("/consultas/", response_model=List[dict])
def obtener_consultas(db: Session = Depends(get_db)):
    consultas = db.query(models.Consulta).order_by(models.Consulta.fecha_hora).all()
    return [
        {
            "id": c.id_consulta,
            "cliente": c.id_cliente,
            "mascota": c.id_mascota,
            "veterinario": c.id_vet,
            "recepcionista": c.id_recepcionista,
            "fecha_hora": c.fecha_hora,
            "motivo": c.motivo
        }
        for c in consultas
    ]

@router.put("/consultas/{id}", response_model=dict)
def actualizar_consulta(id: int, consulta: ConsultaUpdate, db: Session = Depends(get_db)):
    db_consulta = db.query(models.Consulta).filter_by(id_consulta=id).first()
    if not db_consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

    for campo, valor in consulta.dict(exclude_unset=True).items():
        setattr(db_consulta, campo, valor)

    db.commit()
    return {"mensaje": "Consulta actualizada"}

@router.delete("/consultas/{id}", response_model=dict)
def eliminar_consulta(id: int, db: Session = Depends(get_db)):
    consulta = db.query(models.Consulta).filter_by(id_consulta=id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

    db.delete(consulta)
    db.commit()
    return {"mensaje": "Consulta eliminada"}
