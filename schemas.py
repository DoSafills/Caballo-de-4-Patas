# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# --- Modelo para crear una mascota ---
class MascotaCreate(BaseModel):
    nombre: str
    raza: str
    sexo: str
    dieta: str
    caracter: str
    habitat: str
    edad: int
    peso: str
    altura: str
    id_vet: Optional[int] = None  # Relación opcional

# --- Modelo para responder con datos de mascota ---
class MascotaResponse(MascotaCreate):
    id_mascota: int

    class Config:
        orm_mode = True  # Permite convertir desde objetos SQLAlchemy

class ConsultaResponse(BaseModel):
    id_consulta: int
    id_mascota: int
    id_vet: int
    id_cliente: int
    id_recepcionista: int
    motivo: str
    fecha_hora: datetime

    class Config:
        orm_mode = True

class ConsultaCreate(BaseModel):
    id_recepcionista: int
    id_mascota: int
    id_vet: int
    id_cliente: int
    motivo: str
    fecha_hora: datetime

class ClienteCreate(BaseModel):
    rut: str
    nombre: str
    apellido: str
    edad: int
    email: str
    tipo: str = "cliente"
    id_cliente: int
    id_mascota: Optional[int] = None

class ClienteResponse(ClienteCreate):
    class Config:
        orm_mode = True

    class Config:
        orm_mode = True

# --- Veterinario ---
class VeterinarioCreate(BaseModel):
    rut: str
    nombre: str
    apellido: str
    edad: int
    email: str
    tipo: str = "veterinario"
    id_vet: int
    especializacion: str
    contrasena: str

class VeterinarioResponse(VeterinarioCreate):
    class Config:
        orm_mode = True

# --- Recepcionista ---
class RecepcionistaCreate(BaseModel):
    rut: str
    nombre: str
    apellido: str
    edad: int
    email: str
    tipo: str = "recepcionista"
    id_recepcionista: int
    contrasena: str

class RecepcionistaResponse(RecepcionistaCreate):
    class Config:
        orm_mode = True

