
from sqlalchemy.orm import Session
from models import Persona, Admin, Recepcionista, Cliente, Veterinario, Mascota, Consulta

# ---------------------
# CRUD Persona (base)
# ---------------------
def crear_persona(db: Session, datos: dict):
    persona = Persona(**datos)
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona

def obtener_persona(db: Session, rut: str):
    return db.query(Persona).filter_by(rut=rut).first()

def actualizar_persona(db: Session, rut: str, nuevos_datos: dict):
    persona = obtener_persona(db, rut)
    if persona:
        for k, v in nuevos_datos.items():
            setattr(persona, k, v)
        db.commit()
        db.refresh(persona)
    return persona

def eliminar_persona(db: Session, rut: str):
    persona = obtener_persona(db, rut)
    if persona:
        db.delete(persona)
        db.commit()
    return persona

# ---------------------
# CRUD Admin
# ---------------------
def crear_admin(db: Session, datos: dict):
    admin = Admin(**datos)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

def obtener_admin(db: Session, id_admin: int):
    return db.query(Admin).filter_by(id_admin=id_admin).first()

def obtener_admin_por_rut(db: Session, rut: str):
    return db.query(Admin).filter(Admin.rut == rut).first()


def actualizar_admin(db: Session, id_admin: int, nuevos_datos: dict):
    admin = obtener_admin(db, id_admin)
    if admin:
        for k, v in nuevos_datos.items():
            setattr(admin, k, v)
        db.commit()
        db.refresh(admin)
    return admin

def eliminar_admin(db: Session, id_admin: int):
    admin = obtener_admin(db, id_admin)
    if admin:
        db.delete(admin)
        db.commit()
    return admin

# ---------------------
# CRUD Recepcionista
# ---------------------
def crear_recepcionista(db: Session, datos: dict):
    recep = Recepcionista(**datos)
    db.add(recep)
    db.commit()
    db.refresh(recep)
    return recep

def obtener_recepcionista(db: Session, id_recepcionista: int):
    return db.query(Recepcionista).filter_by(id_recepcionista=id_recepcionista).first()

def obtener_recepcionista_por_rut(db, rut: str):
    return db.query(Recepcionista).filter(Recepcionista.rut == rut).first()


def actualizar_recepcionista(db: Session, id_recepcionista: int, nuevos_datos: dict):
    recep = obtener_recepcionista(db, id_recepcionista)
    if recep:
        for k, v in nuevos_datos.items():
            setattr(recep, k, v)
        db.commit()
        db.refresh(recep)
    return recep

def eliminar_recepcionista(db: Session, id_recepcionista: int):
    recep = obtener_recepcionista(db, id_recepcionista)
    if recep:
        db.delete(recep)
        db.commit()
    return recep

# ---------------------
# CRUD Cliente
# ---------------------
def crear_cliente(db: Session, datos: dict):
    cliente = Cliente(**datos)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def obtener_cliente(db: Session, id_cliente: int):
    return db.query(Cliente).filter_by(id_cliente=id_cliente).first()

def actualizar_cliente(db: Session, id_cliente: int, nuevos_datos: dict):
    cliente = obtener_cliente(db, id_cliente)
    if cliente:
        for k, v in nuevos_datos.items():
            setattr(cliente, k, v)
        db.commit()
        db.refresh(cliente)
    return cliente

def eliminar_cliente(db: Session, id_cliente: int):
    cliente = obtener_cliente(db, id_cliente)
    if cliente:
        db.delete(cliente)
        db.commit()
    return cliente

# ---------------------
# CRUD Veterinario
# ---------------------
def crear_veterinario(db: Session, datos: dict):
    vet = Veterinario(**datos)
    db.add(vet)
    db.commit()
    db.refresh(vet)
    return vet

def obtener_veterinario(db: Session, id_vet: int):
    return db.query(Veterinario).filter_by(id_vet=id_vet).first()

def obtener_veterinario_por_rut(db, rut: str):
    return db.query(Veterinario).filter(Veterinario.rut == rut).first()

def actualizar_veterinario(db: Session, id_vet: int, nuevos_datos: dict):
    vet = obtener_veterinario(db, id_vet)
    if vet:
        for k, v in nuevos_datos.items():
            setattr(vet, k, v)
        db.commit()
        db.refresh(vet)
    return vet

def eliminar_veterinario(db: Session, id_vet: int):
    vet = obtener_veterinario(db, id_vet)
    if vet:
        db.delete(vet)
        db.commit()
    return vet

# ---------------------
# CRUD Mascota
# ---------------------
def crear_mascota(db: Session, datos: dict):
    mascota = Mascota(**datos)
    db.add(mascota)
    db.commit()
    db.refresh(mascota)
    return mascota

def obtener_mascota(db: Session, id_mascota: int):
    return db.query(Mascota).filter_by(id_mascota=id_mascota).first()

def obtener_mascota_por_nombre(db: Session, nombre: str):
    return db.query(Mascota).filter(Mascota.nombre == nombre).first()


def actualizar_mascota(db: Session, id_mascota: int, nuevos_datos: dict):
    mascota = obtener_mascota(db, id_mascota)
    if mascota:
        for k, v in nuevos_datos.items():
            setattr(mascota, k, v)
        db.commit()
        db.refresh(mascota)
    return mascota

def obtener_mascotas_por_id(db: Session, id_mascota: int):
    return db.query(Mascota).filter_by(id_mascota=id_mascota).first()


def eliminar_mascota(db: Session, id_mascota: int):
    mascota = obtener_mascota(db, id_mascota)
    if mascota:
        db.delete(mascota)
        db.commit()
    return mascota

# ---------------------
# CRUD Consulta
# ---------------------
def crear_consulta(db: Session, datos: dict):
    consulta = Consulta(**datos)
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta

def obtener_consulta(db: Session, id_consulta: int):
    return db.query(Consulta).filter_by(id_consulta=id_consulta).first()

def actualizar_consulta(db: Session, id_consulta: int, nuevos_datos: dict):
    consulta = obtener_consulta(db, id_consulta)
    if consulta:
        for k, v in nuevos_datos.items():
            setattr(consulta, k, v)
        db.commit()
        db.refresh(consulta)
    return consulta

def eliminar_consulta(db: Session, id_consulta: int):
    consulta = obtener_consulta(db, id_consulta)
    if consulta:
        db.delete(consulta)
        db.commit()
    return consulta
