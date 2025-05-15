from sqlalchemy.orm import Session
from models import Admin,Cliente,Consulta,Mascota,Persona,Recepcionista,Veterinario
MODELOS = {
    "admin": Admin,
    "cliente": Cliente,
    "mascota": Mascota,
    "recepcionista": Recepcionista,
    "veterinario": Veterinario
}

#CRUD adminapp
def obtener_usuarios_por_tipo(db: Session, tipo: str):
    if tipo == "todos":
        resultado = []
        for modelo in MODELOS.values():
            resultado.extend(db.query(modelo).all())
        return resultado
    modelo = MODELOS.get(tipo)
    return db.query(modelo).all() if modelo else []

def eliminar_usuario(db: Session, rut: str, tipo: str):
    modelo = MODELOS.get(tipo)
    if not modelo:
        return False
    usuario = db.query(modelo).filter_by(rut=rut).first()
    if usuario:
        db.delete(usuario)
        db.commit()
        return True
    return False

def actualizar_usuario(db: Session, rut: str, tipo: str, nuevos_datos: dict):
    modelo = MODELOS.get(tipo)
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


#CRUD ADMIN

def crear_admin(session: Session, datos: dict):
    persona = Persona(
        rut=datos['rut'],
        nombre=datos['nombre'],
        apellido=datos['apellido'],
        edad=datos['edad'],
        email=datos['email'],
        tipo='admin'
    )
    admin = Admin(
        rut=datos['rut'],
        contrasena=datos['contrasena']
    )
    session.add(persona)
    session.add(admin)
    session.commit()

def crear_usuario(db, tipo, datos):
    persona = Persona(
        rut=datos["rut"],
        nombre=datos["nombre"],
        apellido=datos["apellido"],
        edad=datos["edad"],
        email=datos["email"],
        tipo=tipo
    )
    db.add(persona)
    db.commit()

    if tipo == "admin":
        usuario = Admin(rut=datos["rut"], contrasena=datos["contrasena"])
    elif tipo == "recepcionista":
        usuario = Recepcionista(rut=datos["rut"], contrasena=datos["contrasena"])
    elif tipo == "veterinario":
        usuario = Veterinario(rut=datos["rut"], especializacion=datos["especializacion"], contrasena=datos["contrasena"])
    else:
        return False

    db.add(usuario)
    db.commit()
    return True

def obtener_admin_por_rut(db, rut):
    return db.query(Admin).filter_by(rut=rut).first()

#CRUD VETERINARIO

def obtener_veterinario_por_rut(db, rut):
    return db.query(Veterinario).filter_by(rut=rut).first()


def crear_veterinario(session: Session, datos: dict):
    persona = Persona(
        rut=datos['rut'],
        nombre=datos['nombre'],
        apellido=datos['apellido'],
        edad=datos['edad'],
        email=datos['email'],
        tipo='veterinario'
    )
    veterinario = Veterinario(
        rut=datos['rut'],
        contrasena=datos['contrasena'],
        especializacion=datos['especializacion']
    )
    session.add(persona)
    session.add(veterinario)
    session.commit()

#CRUD RECEPCIONISTA
def crear_recepcionista(session: Session, datos: dict):
    persona = Persona(
        rut=datos['rut'],
        nombre=datos['nombre'],
        apellido=datos['apellido'],
        edad=datos['edad'],
        email=datos['email'],
        tipo='recepcionista'
    )
    recepcionista = Recepcionista(
        rut=datos['rut'],
        contrasena=datos['contrasena']
    )
    session.add(persona)
    session.add(recepcionista)
    session.commit()

def obtener_recepcionista_por_rut(db, rut):
    return db.query(Recepcionista).filter_by(rut=rut).first()