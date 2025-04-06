# crud.py
from .models import Database

class AnimalCRUD:
    def __init__(self):
        self.db = Database()

    def create_animal(self, nombre, especie, cliente_id):
        query = "INSERT INTO animales (nombre, especie, cliente_id) VALUES (?, ?, ?)"
        self.db.cursor.execute(query, (nombre, especie, cliente_id))
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def get_animals_by_client(self, cliente_id):
        query = "SELECT * FROM animales WHERE cliente_id = ?"
        self.db.cursor.execute(query, (cliente_id,))
        return self.db.cursor.fetchall()

    def update_animal(self, animal_id, datos):
        query = '''
            UPDATE animales
            SET nombre = ?, especie = ?, peso = ?, edad = ?, sexo = ?, caracter = ?
            WHERE id = ?
        '''
        self.db.cursor.execute(query, (*datos, animal_id))
        self.db.conn.commit()

    def delete_animal(self, animal_id):
        query = "DELETE FROM animales WHERE id = ?"
        self.db.cursor.execute(query, (animal_id,))
        self.db.conn.commit()

class ClienteCRUD:
    def __init__(self):
        self.db = Database()

    def create_cliente(self, nombre, telefono, email):
        query = "INSERT INTO clientes (nombre, telefono, email) VALUES (?, ?, ?)"
        self.db.cursor.execute(query, (nombre, telefono, email))
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def get_cliente(self, cliente_id):
        query = "SELECT * FROM clientes WHERE id = ?"
        self.db.cursor.execute(query, (cliente_id,))
        return self.db.cursor.fetchone()

    def update_cliente(self, cliente_id, datos):
        query = '''
            UPDATE clientes
            SET nombre = ?, telefono = ?, email = ?
            WHERE id = ?
        '''
        self.db.cursor.execute(query, (*datos, cliente_id))
        self.db.conn.commit()

    def delete_cliente(self, cliente_id):
        query = "DELETE FROM clientes WHERE id = ?"
        self.db.cursor.execute(query, (cliente_id,))
        self.db.conn.commit()
