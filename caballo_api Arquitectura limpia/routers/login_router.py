from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.models import Admin, Veterinario, Recepcionista
from methods.adapter_autenticador import AdapterAutenticadorStrategy
from pydantic import BaseModel

router = APIRouter()

# sistema de sesión simple (en memoria)
sesiones_activas = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    rut: str
    contrasena: str

class LoginResponse(BaseModel):
    mensaje: str
    rol: str
    nombre: str

@router.post("/login", response_model=LoginResponse)
def login_usuario(data: LoginRequest, db: Session = Depends(get_db)):
    autenticador = AdapterAutenticadorStrategy([
        (Admin, "Administrador"),
        (Veterinario, "Veterinario"),
        (Recepcionista, "Recepcionista")
    ])

    resultado = autenticador.autenticar(db, data.rut, data.contrasena)

    if resultado:
        sesiones_activas[data.rut] = resultado["rol"]
        return {
            "mensaje": "login exitoso",
            "rol": resultado["rol"],
            "nombre": resultado["nombre"]
        }

    raise HTTPException(status_code=401, detail="rut o contraseña inválidos")

@router.post("/logout")
def cerrar_sesion(data: LoginRequest):
    if data.rut in sesiones_activas:
        del sesiones_activas[data.rut]
        return {"mensaje": "sesión cerrada exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="no hay sesión activa con ese rut")
