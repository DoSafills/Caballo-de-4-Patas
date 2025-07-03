from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Cliente, Mascota, Consulta
from schemas import ClienteCreate, ClienteResponse, MascotaCreate, MascotaOut, ConsultaCreate, ConsultaResponse, EstadoUpdate

router = APIRouter(prefix="/recepcionista", tags=["recepcionista"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/clientes/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    nuevo = Cliente(**cliente.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/clientes/", response_model=list[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@router.get("/mascotas/cliente/{rut_cliente}", response_model=list[MascotaOut])
def mascotas_de_cliente(rut_cliente: str, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter_by(rut=rut_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db.query(Mascota).filter_by(id_cliente=cliente.id_cliente).all()

@router.put("/mascotas/{nombre}/estado")
def actualizar_estado(nombre: str, estado: EstadoUpdate, db: Session = Depends(get_db)):
    mascota = db.query(Mascota).filter_by(nombre=nombre).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    mascota.estado = estado.estado
    db.commit()
    return {"msg": "Estado actualizado"}

@router.post("/consultas/", response_model=ConsultaResponse)
def crear_consulta(data: ConsultaCreate, db: Session = Depends(get_db)):
    consulta = Consulta(**data.dict())
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta

@router.get("/consultas/", response_model=list[ConsultaResponse])
def obtener_consultas(db: Session = Depends(get_db)):
    return db.query(Consulta).all()

@router.delete("/consultas/{id_consulta}")
def eliminar_consulta(id_consulta: int, db: Session = Depends(get_db)):
    consulta = db.query(Consulta).get(id_consulta)
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    db.delete(consulta)
    db.commit()
    return {"msg": "Consulta eliminada"}

@router.get("/clientes/{rut_cliente}", response_model=ClienteResponse)
def obtener_cliente_por_rut(rut_cliente: str, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter_by(rut=rut_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente
