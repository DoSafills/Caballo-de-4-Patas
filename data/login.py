from sqlalchemy import create_engine, text

# Conectar a la base existente
engine = create_engine("sqlite:///veterinaria.db")
conn = engine.connect()

# Verificar si la columna 'estado' ya existe
result = conn.execute(text("PRAGMA table_info(mascota);"))
columnas = [col[1] for col in result.fetchall()]

if "estado" not in columnas:
    conn.execute(text("ALTER TABLE mascota ADD COLUMN estado TEXT DEFAULT 'Pendiente atención'"))
    print("✅ Columna 'estado' agregada a la tabla 'mascota'.")
else:
    print("ℹ️ La columna 'estado' ya existe.")

conn.close()
