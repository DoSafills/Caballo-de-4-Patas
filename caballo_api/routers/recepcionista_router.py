
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import UsuarioBase, ConsultaCreate, ConsultaUpdate
from database import SessionLocal
from crud import (
    crear_cliente,
    obtener_cliente_por_rut,
    obtener_todos_los_clientes,
    obtener_mascotas_de_cliente,
    crear_consulta,
    obtener_recepcionista_por_rut,
    actualizar_consulta,
    eliminar_consulta,
    actualizar_estado_mascota
)
from pydantic import BaseModel
from datetime import datetime
from typing import List
from models import Consulta


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===================== CLIENTES =====================

@router.post("/clientes/crear", response_model=UsuarioBase)
def crear_cliente_endpoint(datos: UsuarioBase, db: Session = Depends(get_db)):
    cliente = crear_cliente(db, datos.rut, datos.nombre, datos.apellido, datos.edad, datos.email, "")
    if not cliente:
        raise HTTPException(status_code=400, detail="No se pudo crear el cliente")
    return cliente

@router.get("/clientes/", response_model=List[UsuarioBase])
def listar_clientes_endpoint(db: Session = Depends(get_db)):
    return obtener_todos_los_clientes(db)

@router.get("/clientes/{rut}", response_model=UsuarioBase)
def obtener_cliente_endpoint(rut: str, db: Session = Depends(get_db)):
    cliente = obtener_cliente_por_rut(db, rut)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.get("/clientes/{rut}/mascotas")
def listar_mascotas_cliente(rut: str, db: Session = Depends(get_db)):
    cliente = obtener_cliente_por_rut(db, rut)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    mascotas = obtener_mascotas_de_cliente(db, cliente.id_cliente)
    return [{"id": m.id_mascota, "nombre": m.nombre, "estado": m.estado} for m in mascotas]

# ===================== CONSULTAS =====================

@router.post("/consultas/crear")
def agendar_consulta_endpoint(datos: ConsultaCreate, db: Session = Depends(get_db)):
    if not obtener_recepcionista_por_rut(db, str(datos.id_recepcionista)):
        raise HTTPException(status_code=404, detail="Recepcionista no encontrado")
    nueva = crear_consulta(
        db,
        datos.fecha_hora,
        datos.id_recepcionista,
        datos.id_mascota,
        datos.id_vet,
        datos.id_cliente,
        datos.motivo
    )
    if not nueva:
        raise HTTPException(status_code=400, detail="No se pudo agendar la consulta")
    return {"mensaje": "Consulta creada", "id": nueva.id_consulta}

@router.get("/consultas/", response_model=List[dict])
def listar_consultas_endpoint(db: Session = Depends(get_db)):
    consultas = db.query(Consulta).order_by(Consulta.fecha_hora).all()
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

@router.put("/consultas/{id}")
def actualizar_consulta_endpoint(id: int, datos: ConsultaUpdate, db: Session = Depends(get_db)):
    actual = actualizar_consulta(db, id, datos.dict(exclude_unset=True))
    if not actual:
        raise HTTPException(status_code=404, detail="Consulta no encontrada o no actualizada")
    return {"mensaje": "Consulta actualizada", "id": actual.id_consulta}

@router.delete("/consultas/{id}")
def eliminar_consulta_endpoint(id: int, db: Session = Depends(get_db)):
    ok = eliminar_consulta(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    return {"mensaje": "Consulta eliminada"}

# ===================== ESTADO DE MASCOTA =====================

class EstadoUpdate(BaseModel):
    estado: str

@router.put("/mascotas/{id_mascota}/estado")
def actualizar_estado_endpoint(id_mascota: int, payload: EstadoUpdate, db: Session = Depends(get_db)):
    m = actualizar_estado_mascota(db, id_mascota, payload.estado)
    if not m:
        raise HTTPException(status_code=404, detail="Mascota no encontrada o no se pudo actualizar")
    return {"mensaje": "Estado actualizado", "id_mascota": m.id_mascota, "nuevo_estado": m.estado}
