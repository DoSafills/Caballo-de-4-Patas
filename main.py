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

    try:
        # Insertar un veterinario de prueba
        logging.info("Insertando veterinario de prueba...")
        vet = crud.crear_veterinario(db, "12345678-9", "Juan", "Pérez", 40, "Cirugía", "contraseña")
        if vet:
            logging.info(f"Veterinario creado: {vet.nombre} {vet.apellido}")
        else:
            logging.error("Error al crear el veterinario.")

        # Insertar una mascota asociada al veterinario
        logging.info("Insertando mascota de prueba...")
        mascota = crud.crear_mascota(db, "CHP001", "Firulais", "Labrador", "Macho", "Carnívora", "Amigable", "Casa", 5, "25kg", "60cm", "12345678-9")
        if mascota:
            vet_name = mascota.veterinario.nombre if mascota.veterinario else "Veterinario no asignado"
            logging.info(f"Mascota creada: {mascota.nombre}, atendida por {vet_name}")
        else:
            logging.error("Error al crear la mascota.")

        # Obtener y mostrar todos los veterinarios
        veterinarios = crud.obtener_veterinarios(db)
        logging.info(f"Veterinarios registrados: {[v.nombre for v in veterinarios]}")

        # Obtener y mostrar todas las mascotas
        mascotas = crud.obtener_mascotas(db)
        logging.info(f"Mascotas registradas: {[m.nombre for m in mascotas]}")

        # Actualizar un veterinario
        logging.info("Actualizando especialización del veterinario...")
        vet_actualizado = crud.actualizar_veterinario(db, "12345678-9", especializacion="Oncología")
        if vet_actualizado:
            logging.info(f"Veterinario actualizado: {vet_actualizado.nombre}, nueva especialización: {vet_actualizado.especializacion}")
        else:
            logging.error("Error al actualizar el veterinario.")

        # Eliminar una mascota
        logging.info("Eliminando una mascota...")
        if crud.eliminar_mascota(db, "CHP001"):
            logging.info("Mascota eliminada correctamente.")
        else:
            logging.error("Error al eliminar la mascota.")

    except Exception as e:
        logging.error(f"Error inesperado: {e}")

    finally:
        # Cerrar sesión de la base de datos
        db.close()
        logging.info("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    main()
