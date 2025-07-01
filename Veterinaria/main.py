# main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session

from Veterinaria.database import engine
import Veterinaria.models as models
import Veterinaria.schemas as schemas

from fastapi import Body
from Veterinaria.services import mascota_service
from Veterinaria.services import consulta_service

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "API de Veterinaria operativa"}

@app.post("/mascotas", response_model=schemas.MascotaResponse)
def crear_mascota(mascota: schemas.MascotaCreate):
    return mascota_service.crear_mascota(mascota)

@app.get("/mascotas", response_model=list[schemas.MascotaResponse])
def obtener_mascotas():
    return mascota_service.obtener_mascotas()

@app.put("/mascotas/{id_mascota}", response_model=schemas.MascotaResponse)
def actualizar_mascota(id_mascota: int, datos: schemas.MascotaUpdate):
    return mascota_service.actualizar_mascota(id_mascota, datos)

@app.post("/historial", response_model=schemas.ConsultaResponse)
def crear_consulta(consulta: schemas.ConsultaCreate):
    return consulta_service.crear_consulta(**consulta.dict())

@app.get("/historial/{id_mascota}", response_model=list[schemas.ConsultaResponse])
def historial_mascota(id_mascota: int):
    return consulta_service.listar_por_mascota(id_mascota)

# @app.post("/clientes", response_model=schemas.ClienteResponse)
# def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
#     nuevo_cliente = models.Cliente(**cliente.dict())
#     db.add(nuevo_cliente)
#     db.commit()
#     db.refresh(nuevo_cliente)
#     return nuevo_cliente

# @app.get("/clientes", response_model=list[schemas.ClienteResponse])
# def obtener_clientes(db: Session = Depends(get_db)):
#     return db.query(models.Cliente).all()

# @app.post("/veterinarios", response_model=schemas.VeterinarioResponse)
# def crear_veterinario(vet: schemas.VeterinarioCreate, db: Session = Depends(get_db)):
#     nuevo = models.Veterinario(**vet.dict())
#     db.add(nuevo)
#     db.commit()
#     db.refresh(nuevo)
#     return nuevo

# @app.get("/veterinarios", response_model=list[schemas.VeterinarioResponse])
# def obtener_veterinarios(db: Session = Depends(get_db)):
#     return db.query(models.Veterinario).all()

# @app.post("/recepcionistas", response_model=schemas.RecepcionistaResponse)
# def crear_recepcionista(recepcionista: schemas.RecepcionistaCreate, db: Session = Depends(get_db)):
#     nuevo = models.Recepcionista(**recepcionista.dict())
#     db.add(nuevo)
#     db.commit()
#     db.refresh(nuevo)
#     return nuevo

# @app.get("/recepcionistas", response_model=list[schemas.RecepcionistaResponse])
# def obtener_recepcionistas(db: Session = Depends(get_db)):
#     return db.query(models.Recepcionista).all()
