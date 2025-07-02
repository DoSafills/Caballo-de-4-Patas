from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class UsuarioBase(BaseModel):
    rut: str
    nombre: str
    apellido: str
    edad: int
    email: str
    contrasena: str

class UsuarioCreate(UsuarioBase):
    tipo: str
    especializacion: Optional[str] = None

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    email: Optional[str] = None
    contrasena: Optional[str] = None



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
    id_cliente: Optional[int] = None

class MascotaOut(MascotaCreate):
    id_mascota: int

    class Config:
        orm_mode = True

class ClienteOut(UsuarioBase):
    id_cliente: int
    class Config:
        orm_mode = True

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

class ConsultaOut(ConsultaCreate):
    id_consulta: int
    class Config:
        orm_mode = True