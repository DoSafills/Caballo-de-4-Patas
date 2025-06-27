# main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from fastapi import Depends, HTTPException
import schemas
from fastapi import Body


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Conexión a DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"mensaje": "API de Veterinaria operativa"}

# Ruta POST: registrar mascota
@app.post("/mascotas", response_model=schemas.MascotaResponse)
def crear_mascota(mascota: schemas.MascotaCreate, db: Session = Depends(get_db)):
    nueva = models.Mascota(**mascota.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# Ruta GET: listar mascotas
@app.get("/mascotas", response_model=list[schemas.MascotaResponse])
def obtener_mascotas(db: Session = Depends(get_db)):
    return db.query(models.Mascota).all()

@app.get("/historial/{id_mascota}", response_model=list[schemas.ConsultaResponse])
def historial_mascota(id_mascota: int, db: Session = Depends(get_db)):
    historial = db.query(models.Consulta).filter(models.Consulta.id_mascota == id_mascota).all()
    if not historial:
        raise HTTPException(status_code=404, detail="No se encontró historial para esa mascota")
    return historial

@app.post("/historial", response_model=schemas.ConsultaResponse)
def crear_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    nueva = models.Consulta(**consulta.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.post("/clientes", response_model=schemas.ClienteResponse)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    nuevo_cliente = models.Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@app.get("/clientes", response_model=list[schemas.ClienteResponse])
def obtener_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()
