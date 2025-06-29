from database import SessionLocal, inicializar_base
from models import Admin, Cliente, Veterinario, Mascota
from datetime import datetime

# Inicializar base de datos
inicializar_base()
db = SessionLocal()

# Función para agregar datos
def agregar_datos():
    try:
        # Crear un administrador
        admin = Admin(
            rut="22334455-6",
            nombre="Pepe",
            apellido="Tapia",
            edad=30,
            email="ptapia@example.com",
            contrasena="clave123"
        )
        db.add(admin)

        # Crear un cliente
        cliente = Cliente(
            rut="12345678-9",
            nombre="Camila",
            apellido="López",
            edad=30,
            email="camila@example.com",
        )
        db.add(cliente)

        # Crear un veterinario
        veterinario = Veterinario(
            rut="11223344-5",
            nombre="Dr. Ramírez",
            apellido="Pérez",
            edad=45,
            especializacion="Cirugía",
            contrasena="segura123"
        )
        db.add(veterinario)

        # Crear una mascota
        mascota = Mascota(
            nombre="Luna",
            raza="Golden Retriever",
            sexo="Hembra",
            dieta="Especial",
            caracter="Activa",
            habitat="Casa",
            id_vet=veterinario.id_vet,
            edad=5,
            peso="30kg",
            altura="60cm"
        )
        db.add(mascota)

        # Commit para guardar los datos
        db.commit()

        print("Datos agregados correctamente.")
    except Exception as e:
        # Si ocurre un error, deshacer todo lo que se haya hecho
        db.rollback()
        print(f"Error al agregar datos: {e}")

# Llamada a la función para agregar los datos
agregar_datos()
