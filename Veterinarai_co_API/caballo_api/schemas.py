from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from typing import Optional


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
        from_attributes = True

class HistorialCreate(BaseModel):
    descripcion: str
    id_mascota: int

class MascotaUpdate(BaseModel):
    edad: Optional[int]
    sexo: Optional[str]
    estado: Optional[str]  # Esto si lo manejas desde la interfaz

    class Config:
        from_attributes = True
