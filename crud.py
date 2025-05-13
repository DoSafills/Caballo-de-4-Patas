from sqlalchemy.orm import Session
from models import Admin, Cliente, Consulta, Mascota, Usuario, Recepcionista, Veterinario

#CRUD ADMIN

def crear_admin(db, admin_data):
    nuevo_admin = Admin(**admin_data)
    db.add(nuevo_admin)
    db.commit()
    db.refresh(nuevo_admin)
    return nuevo_admin

def crear_admin_NE(db: Session, datos: dict):
    existente = obtener_admin_por_rut(db, datos["rut"])
    if existente:
        return existente
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

def eliminar_admin_por_rut(db, rut):
    admin = db.query(Admin).filter_by(rut=rut).first()
    if admin:
        db.delete(admin)
        db.commit()
        return True
    return False

#CRUD USUARIO

def crear_usuario(db: Session, datos: dict):
    existente = obtener_usuario(db, datos["rut"])
    if existente:
        return existente
    usuario = Usuario(**datos)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def obtener_usuario(db: Session, rut: str):
    return db.query(Usuario).filter_by(rut=rut).first()

def actualizar_usuario(db: Session, rut: str, nuevos_datos: dict):
    usuario = obtener_usuario(db, rut)
    if usuario:
        for k, v in nuevos_datos.items():
            setattr(usuario, k, v)
        db.commit()
        db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, rut: str):
    usuario = obtener_usuario(db, rut)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario

#CRUD CLIENTE

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


#CRUD CONSULTA

def crear_consulta(db: Session, datos: dict):
    consulta_existente = db.query(Consulta).filter_by(
        fecha_hora=datos["fecha_hora"],
        id_mascota=datos["id_mascota"],
        id_vet=datos["id_vet"]
    ).first()
    if consulta_existente:
        return consulta_existente
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

#CRUD MASCOTA

def crear_mascota(db: Session, datos: dict):
    existente = obtener_mascota_por_nombre(db, datos["nombre"])
    if existente:
        return existente
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

#CRUD RECEPCIONISTA

def crear_recepcionista(db, recepcionista_data):
    nuevo_recepcionista = Recepcionista(**recepcionista_data)
    db.add(nuevo_recepcionista)
    db.commit()
    db.refresh(nuevo_recepcionista)
    return nuevo_recepcionista


def crear_recepcionista_NE(db: Session, datos: dict):
    existente = obtener_recepcionista_por_rut(db, datos["rut"])
    if existente:
        return existente
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

def eliminar_recepcionista_por_rut(db, rut):
    recep = db.query(Recepcionista).filter_by(rut=rut).first()
    if recep:
        db.delete(recep)
        db.commit()
        return True
    return False


#CRUD VETERINARIO

def crear_veterinario(db, vet_data):
    nuevo_vet = Veterinario(**vet_data)
    db.add(nuevo_vet)
    db.commit()
    db.refresh(nuevo_vet)
    return nuevo_vet


def crear_veterinario_NE(db: Session, datos: dict):
    existente = obtener_veterinario_por_rut(db, datos["rut"])
    if existente:
        return existente
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

def eliminar_veterinario_por_rut(db, rut):
    vet = db.query(Veterinario).filter_by(rut=rut).first()
    if vet:
        db.delete(vet)
        db.commit()
        return True
    return False

