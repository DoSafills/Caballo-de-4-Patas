from pydantic import BaseModel
from typing import Optional

# schemas.py

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
