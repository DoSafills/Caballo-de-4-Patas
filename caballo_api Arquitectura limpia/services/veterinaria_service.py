from sqlalchemy.orm import Session
from models.models import Mascota, Cliente

def registrar_mascota_service(db: Session, datos: dict):
    mascota = Mascota(
        nombre=datos["nombre"],
        raza=datos["raza"],
        sexo=datos["sexo"],
        dieta=datos["dieta"],
        caracter=datos["caracter"],
        habitat=datos["habitat"],
        edad=int(datos["edad"]),
        peso=datos["peso"],
        altura=datos["altura"],
        id_cliente=datos.get("id_cliente")  # opcional
    )
    db.add(mascota)
    db.commit()
    db.refresh(mascota)
    return mascota

def obtener_mascotas_service(db: Session):
    return db.query(Mascota).all()

def obtener_mascotas_por_cliente(db: Session, id_cliente: int):
    return db.query(Mascota).filter(Mascota.id_cliente == id_cliente).all()
