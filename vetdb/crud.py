from sqlalchemy.orm import Session
from models import Veterinario, Mascota

# ---------------------- CRUD Veterinario ----------------------

def crear_veterinario(db: Session, rut: str, nombre: str, apellido: str, edad: int, especializacion: str):
    """Crea un nuevo veterinario en la base de datos."""
    nuevo_veterinario = Veterinario(
        rut_veterinario=rut,
        nombre=nombre,
        apellido=apellido,
        edad=edad,
        especializacion=especializacion
    )
    db.add(nuevo_veterinario)
    db.commit()
    db.refresh(nuevo_veterinario)
    return nuevo_veterinario

def obtener_veterinarios(db: Session):
    """Obtiene todos los veterinarios registrados."""
    return db.query(Veterinario).all()

def obtener_veterinario_por_rut(db: Session, rut: str):
    """Obtiene un veterinario por su RUT."""
    return db.query(Veterinario).filter(Veterinario.rut_veterinario == rut).first()

def actualizar_veterinario(db: Session, rut: str, nombre: str = None, apellido: str = None, edad: int = None, especializacion: str = None):
    """Actualiza los datos de un veterinario."""
    veterinario = obtener_veterinario_por_rut(db, rut)
    if not veterinario:
        return None
    if nombre:
        veterinario.nombre = nombre
    if apellido:
        veterinario.apellido = apellido
    if edad:
        veterinario.edad = edad
    if especializacion:
        veterinario.especializacion = especializacion
    db.commit()
    db.refresh(veterinario)
    return veterinario

def eliminar_veterinario(db: Session, rut: str):
    """Elimina un veterinario de la base de datos."""
    veterinario = obtener_veterinario_por_rut(db, rut)
    if veterinario:
        db.delete(veterinario)
        db.commit()
    return veterinario

# ---------------------- CRUD Mascota ----------------------

def crear_mascota(db: Session, chapa: str, nombre: str, raza: str, sexo: str, dieta: str, caracter: str, habitat: str, edad: int, peso: str, altura: str, rut_veterinario: str = None):
    """Crea una nueva mascota en la base de datos."""
    nueva_mascota = Mascota(
        chapa=chapa,
        nombre=nombre,
        raza=raza,
        sexo=sexo,
        dieta=dieta,
        caracter=caracter,
        habitat=habitat,
        edad=edad,
        peso=peso,
        altura=altura,
        rut_veterinario=rut_veterinario
    )
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota

def obtener_mascotas(db: Session):
    """Obtiene todas las mascotas registradas."""
    return db.query(Mascota).all()

def obtener_mascota_por_chapa(db: Session, chapa: str):
    """Obtiene una mascota por su chapa."""
    return db.query(Mascota).filter(Mascota.chapa == chapa).first()

def actualizar_mascota(db: Session, chapa: str, nombre: str = None, raza: str = None, sexo: str = None, dieta: str = None, caracter: str = None, habitat: str = None, edad: int = None, peso: str = None, altura: str = None, rut_veterinario: str = None):
    """Actualiza los datos de una mascota."""
    mascota = obtener_mascota_por_chapa(db, chapa)
    if not mascota:
        return None
    if nombre:
        mascota.nombre = nombre
    if raza:
        mascota.raza = raza
    if sexo:
        mascota.sexo = sexo
    if dieta:
        mascota.dieta = dieta
    if caracter:
        mascota.caracter = caracter
    if habitat:
        mascota.habitat = habitat
    if edad:
        mascota.edad = edad
    if peso:
        mascota.peso = peso
    if altura:
        mascota.altura = altura
    if rut_veterinario:
        mascota.rut_veterinario = rut_veterinario
    db.commit()
    db.refresh(mascota)
    return mascota

def eliminar_mascota(db: Session, chapa: str):
    """Elimina una mascota de la base de datos."""
    mascota = obtener_mascota_por_chapa(db, chapa)
    if mascota:
        db.delete(mascota)
        db.commit()
    return mascota
