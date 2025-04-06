import sqlite3

class Database:
    def __init__(self, db_name='veterinaria.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        schemas = [
            '''CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS animales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especie TEXT,
                peso REAL,
                edad INTEGER,
                sexo TEXT,
                caracter TEXT,
                cliente_id INTEGER,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )'''
            # Añade más tablas según sea necesario
        ]

        for schema in schemas:
            self.cursor.execute(schema)
        self.conn.commit()
