
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from entities.schemas import UsuarioCreate, UsuarioUpdate
from services.admin_service import crear_usuario_service, actualizar_usuario_service, eliminar_usuario_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/crear")
def crear_usuario_endpoint(datos: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = crear_usuario_service(db, datos)
    if not usuario:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
    return usuario


@router.put("/actualizar/{tipo}/{rut}")
def actualizar_usuario_endpoint(tipo: str, rut: str, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = actualizar_usuario_service(db, tipo, rut, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no actualizado")
    return usuario

@router.delete("/eliminar/{tipo}/{rut}")
def eliminar_usuario_endpoint(tipo: str, rut: str, db: Session = Depends(get_db)):
    exito = eliminar_usuario_service(db, tipo, rut)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no eliminado")
    return {"mensaje": "Usuario eliminado correctamente"}

@router.get("/usuarios/{tipo}")
def obtener_usuarios(tipo: str, db: Session = Depends(get_db)):
    from use_cases.crud import obtener_usuarios_por_tipo  
    usuarios = obtener_usuarios_por_tipo(db, tipo)
    if usuarios is None:
        raise HTTPException(status_code=404, detail="Tipo de usuario no válido")
    return usuarios
