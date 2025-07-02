from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from caballo_api.database import get_db
from caballo_api.schemas import (
    UsuarioBase,
    ConsultaCreate,
    ConsultaUpdate,
    ClienteOut,
    ConsultaOut
)
from caballo_api.services.recepcionista_service import RecepcionistaService

router = APIRouter(prefix="/recepcionista", tags=["Recepcionista"])

@router.post("/clientes/", response_model=ClienteOut)
def crear_cliente_api(cliente: UsuarioBase, db: Session = Depends(get_db)):
    service = RecepcionistaService(db)
    try:
        nuevo = service.crear_cliente(
            rut=cliente.rut,
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            edad=cliente.edad,
            email=cliente.email
        )
        return nuevo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clientes/", response_model=List[ClienteOut])
def listar_clientes_api(db: Session = Depends(get_db)):
    return RecepcionistaService(db).listar_clientes()

@router.get("/clientes/{rut}", response_model=ClienteOut)
def obtener_cliente_api(rut: str, db: Session = Depends(get_db)):
    try:
        return RecepcionistaService(db).obtener_cliente(rut)
    except LookupError:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.post("/consultas/", response_model=ConsultaOut)
def agendar_consulta_api(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    try:
        return RecepcionistaService(db).agendar_consulta(**consulta.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/consultas/", response_model=List[ConsultaOut])
def listar_consultas_api(db: Session = Depends(get_db)):
    return RecepcionistaService(db).listar_consultas()

@router.put("/consultas/{id}", response_model=ConsultaOut)
def actualizar_consulta_api(id: int, consulta: ConsultaUpdate, db: Session = Depends(get_db)):
    try:
        return RecepcionistaService(db).actualizar_consulta(id, **consulta.dict(exclude_unset=True))
    except LookupError:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")

@router.delete("/consultas/{id}", status_code=204)
def eliminar_consulta_api(id: int, db: Session = Depends(get_db)):
    try:
        RecepcionistaService(db).eliminar_consulta(id)
    except LookupError:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
