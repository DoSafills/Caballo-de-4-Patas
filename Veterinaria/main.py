# main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session
from Veterinaria.database import SessionLocal, engine
import Veterinaria.models as models
from fastapi import Depends, HTTPException
import Veterinaria.schemas as schemas
from fastapi import Body
from Veterinaria.services import mascota_service

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
    return mascota_service.crear_mascota(db, mascota)

@app.get("/mascotas", response_model=list[schemas.MascotaResponse])
def obtener_mascotas(db: Session = Depends(get_db)):
    return mascota_service.obtener_mascotas(db)

@app.put("/mascotas/{id_mascota}", response_model=schemas.MascotaResponse)
def actualizar_mascota(id_mascota: int, datos: schemas.MascotaUpdate, db: Session = Depends(get_db)):
    return mascota_service.actualizar_mascota(db, id_mascota, datos)

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

@app.post("/veterinarios", response_model=schemas.VeterinarioResponse)
def crear_veterinario(vet: schemas.VeterinarioCreate, db: Session = Depends(get_db)):
    nuevo = models.Veterinario(**vet.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/veterinarios", response_model=list[schemas.VeterinarioResponse])
def obtener_veterinarios(db: Session = Depends(get_db)):
    return db.query(models.Veterinario).all()

@app.post("/recepcionistas", response_model=schemas.RecepcionistaResponse)
def crear_recepcionista(recepcionista: schemas.RecepcionistaCreate, db: Session = Depends(get_db)):
    nuevo = models.Recepcionista(**recepcionista.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/recepcionistas", response_model=list[schemas.RecepcionistaResponse])
def obtener_recepcionistas(db: Session = Depends(get_db)):
    return db.query(models.Recepcionista).all()
