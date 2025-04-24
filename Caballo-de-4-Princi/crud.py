from sqlalchemy.orm import Session
from models import Veterinario, Mascota
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# ---------------------- CRUD Veterinario ----------------------

def crear_veterinario(db: Session, rut: str, nombre: str, apellido: str, edad: int, especializacion: str, contrasena: str):
    """Crea un nuevo veterinario en la base de datos."""
    try:
        nuevo_veterinario = Veterinario(
            rut_veterinario=rut,
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            especializacion=especializacion,
            contrasena=contrasena
        )
        db.add(nuevo_veterinario)
        db.commit()
        db.refresh(nuevo_veterinario)
        return nuevo_veterinario
    except IntegrityError:
        db.rollback()
        print(f"Error: Ya existe un veterinario con el RUT {rut}.")
        return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear veterinario: {e}")
        return None

def obtener_veterinarios(db: Session):
    """Obtiene todos los veterinarios registrados."""
    return db.query(Veterinario).all()

def obtener_veterinario_por_rut(db: Session, rut: str):
    """Obtiene un veterinario por su RUT."""
    return db.query(Veterinario).filter(Veterinario.rut_veterinario == rut).first()

def actualizar_veterinario(db: Session, rut: str, nombre: str = None, apellido: str = None, edad: int = None, especializacion: str = None, contrasena: str = None):
    """Actualiza los datos de un veterinario."""
    veterinario = obtener_veterinario_por_rut(db, rut)
    if not veterinario:
        print(f"Error: Veterinario con RUT {rut} no encontrado.")
        return None
    try:
        if nombre: veterinario.nombre = nombre
        if apellido: veterinario.apellido = apellido
        if edad: veterinario.edad = edad
        if especializacion: veterinario.especializacion = especializacion
        if contrasena: veterinario.contrasena = contrasena
        db.commit()
        db.refresh(veterinario)
        return veterinario
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al actualizar veterinario: {e}")
        return None

def eliminar_veterinario(db: Session, rut: str):
    """Elimina un veterinario solo si no tiene mascotas asignadas."""
    veterinario = obtener_veterinario_por_rut(db, rut)
    if not veterinario:
        print(f"Error: Veterinario con RUT {rut} no encontrado.")
        return None
    if veterinario.mascotas:
        print("No se puede eliminar el veterinario porque tiene mascotas asignadas.")
        return None
    try:
        db.delete(veterinario)
        db.commit()
        return veterinario
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al eliminar veterinario: {e}")
        return None

# ---------------------- CRUD Mascota ----------------------

def crear_mascota(db: Session, chapa: str, nombre: str, raza: str, sexo: str, dieta: str, caracter: str, habitat: str, edad: int, peso: str, altura: str, rut_veterinario: str = None):
    """Crea una nueva mascota solo si el veterinario existe (si se indica uno)."""
    if rut_veterinario:
        veterinario = obtener_veterinario_por_rut(db, rut_veterinario)
        if not veterinario:
            print(f"Error: Veterinario con RUT {rut_veterinario} no existe.")
            return None
    try:
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
    except IntegrityError:
        db.rollback()
        print(f"Error: Ya existe una mascota con la chapa {chapa}.")
        return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear mascota: {e}")
        return None

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
        print(f"Error: Mascota con chapa {chapa} no encontrada.")
        return None
    if rut_veterinario:
        veterinario = obtener_veterinario_por_rut(db, rut_veterinario)
        if not veterinario:
            print(f"Error: Veterinario con RUT {rut_veterinario} no existe.")
            return None
    try:
        if nombre: mascota.nombre = nombre
        if raza: mascota.raza = raza
        if sexo: mascota.sexo = sexo
        if dieta: mascota.dieta = dieta
        if caracter: mascota.caracter = caracter
        if habitat: mascota.habitat = habitat
        if edad: mascota.edad = edad
        if peso: mascota.peso = peso
        if altura: mascota.altura = altura
        if rut_veterinario: mascota.rut_veterinario = rut_veterinario
        db.commit()
        db.refresh(mascota)
        return mascota
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al actualizar mascota: {e}")
        return None

def eliminar_mascota(db: Session, chapa: str):
    """Elimina una mascota de la base de datos."""
    mascota = obtener_mascota_por_chapa(db, chapa)
    if not mascota:
        print(f"Error: Mascota con chapa {chapa} no encontrada.")
        return None
    try:
        db.delete(mascota)
        db.commit()
        return mascota
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al eliminar mascota: {e}")
        return None
