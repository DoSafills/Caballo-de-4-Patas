from sqlalchemy.orm import Session
from models import Admin, Cliente, Cita, Mascota, Usuario, Recepcionista, Veterinario

MODELOS = {
    "admin": Admin,
    "cliente": Cliente,
    "mascota": Mascota,
    "recepcionista": Recepcionista,
    "veterinario": Veterinario
}

# CRUD adminapp
def obtener_usuarios_por_rol(db: Session, rol: str):
    if rol == "todos":
        resultado = []
        for modelo in MODELOS.values():
            resultado.extend(db.query(modelo).all())
        return resultado
    modelo = MODELOS.get(rol)
    return db.query(modelo).all() if modelo else []

def eliminar_usuario(db: Session, rut: str, rol: str):
    modelo = MODELOS.get(rol)
    if not modelo:
        return False
    usuario = db.query(modelo).filter_by(rut=rut).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return True
    return False

def actualizar_usuario(db: Session, rut: str, rol: str, nuevos_datos: dict):
    modelo = MODELOS.get(rol)
    if not modelo:
        return None
    usuario = db.query(modelo).filter_by(rut=rut).first()
    if usuario:
        for k, v in nuevos_datos.items():
            setattr(usuario, k, v)
        db.commit()
        db.refresh(usuario)
        return usuario
    return None

def crear_usuario(db, rol, datos):
    try:
        if rol == "admin":
            usuario = Admin(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                rol="admin",
                contrasena=datos["contrasena"]
            )
        elif rol == "recepcionista":
            usuario = Recepcionista(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                rol="recepcionista",
                contrasena=datos["contrasena"]
            )
        elif rol == "veterinario":
            usuario = Veterinario(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                rol="veterinario",
                contrasena=datos["contrasena"],
                especializacion=datos["especializacion"]
            )
        else:
            return False

        db.add(usuario)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"error al crear usuario: {e}")
        return False

def obtener_admin_por_rut(db, rut):
    return db.query(Admin).filter_by(rut=rut).first()

def obtener_veterinario_por_rut(db, rut):
    return db.query(Veterinario).filter_by(rut=rut).first()

def obtener_recepcionista_por_rut(db, rut):
    return db.query(Recepcionista).filter_by(rut=rut).first()
