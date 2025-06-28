import sqlite3

# Conexión
conn = sqlite3.connect("veterinaria.db")
cursor = conn.cursor()

# Limpiar datos previos
cursor.execute("DELETE FROM admin")
cursor.execute("DELETE FROM recepcionista")
cursor.execute("DELETE FROM veterinario")
cursor.execute("DELETE FROM cliente")
cursor.execute("DELETE FROM persona")

# Insertar personas base
personas = [
    ("11-1", "Alicia", "Admin", 35, "admin@vet.cl", "admin"),
    ("22-2", "Ricardo", "Recep", 28, "recep@vet.cl", "recepcionista"),
    ("33-3", "Valentina", "Vet", 40, "vet@vet.cl", "veterinario"),
    ("44-4", "Carlos", "Cliente", 31, "cliente@vet.cl", "cliente")
]
cursor.executemany("""
    INSERT INTO persona (rut, nombre, apellido, edad, email, tipo)
    VALUES (?, ?, ?, ?, ?, ?)
""", personas)

# Insertar usuarios con contraseñas
cursor.execute("INSERT INTO admin (id_admin, contrasena, rut) VALUES (1, 'admin123', '11-1')")
cursor.execute("INSERT INTO recepcionista (id_recepcionista, contrasena, rut) VALUES (1, 'recep123', '22-2')")
cursor.execute("INSERT INTO veterinario (id_vet, rut, especializacion, contrasena) VALUES (1, '33-3', 'Exóticos', 'vet123')")
cursor.execute("INSERT INTO cliente (id_cliente, rut) VALUES (1, '44-4')")

# Guardar y cerrar
conn.commit()
conn.close()

print("✅ Datos de prueba cargados exitosamente.")
