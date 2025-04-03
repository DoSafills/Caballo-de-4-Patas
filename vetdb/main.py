import logging
from database import init_db, SessionLocal
import crud

# Configuración del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    # Inicializar la base de datos
    init_db()

    # Crear una sesión de base de datos
    db = SessionLocal()

    # Insertar un veterinario de prueba
    logging.info("Insertando veterinario de prueba...")
    vet = crud.crear_veterinario(db, "12345678-9", "Juan", "Pérez", 40, "Cirugía")
    logging.info(f"Veterinario creado: {vet.nombre} {vet.apellido}")

    # Insertar una mascota asociada al veterinario
    logging.info("Insertando mascota de prueba...")
    mascota = crud.crear_mascota(db, "CHP001", "Firulais", "Labrador", "Macho", "Carnívora", "Amigable", "Casa", 5, "25kg", "60cm", "12345678-9")
    logging.info(f"Mascota creada: {mascota.nombre}, atendida por {mascota.veterinario.nombre}")

    # Obtener y mostrar todos los veterinarios
    veterinarios = crud.obtener_veterinarios(db)
    logging.info(f"Veterinarios registrados: {[v.nombre for v in veterinarios]}")

    # Obtener y mostrar todas las mascotas
    mascotas = crud.obtener_mascotas(db)
    logging.info(f"Mascotas registradas: {[m.nombre for m in mascotas]}")

    # Actualizar un veterinario
    logging.info("Actualizando especialización del veterinario...")
    vet_actualizado = crud.actualizar_veterinario(db, "12345678-9", especializacion="Oncología")
    logging.info(f"Veterinario actualizado: {vet_actualizado.nombre}, nueva especialización: {vet_actualizado.especializacion}")

    # Eliminar una mascota
    logging.info("Eliminando una mascota...")
    crud.eliminar_mascota(db, "CHP001")
    logging.info("Mascota eliminada.")

    # Cerrar sesión de la base de datos
    db.close()

if __name__ == "__main__":
    main()
