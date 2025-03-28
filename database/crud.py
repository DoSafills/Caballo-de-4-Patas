from .models import Database

class AnimalCRUD:
    def __init__(self):
        self.db = Database()
    
    def create_animal(self, nombre, especie, cliente_id):
        self.db.cursor.execute(
            "INSERT INTO animales (nombre, especie, cliente_id) VALUES (?, ?, ?)",
            (nombre, especie, cliente_id)
        )
        self.db.conn.commit()
        return self.db.cursor.lastrowid
    
    def get_animals_by_client(self, cliente_id):
        self.db.cursor.execute(
            "SELECT * FROM animales WHERE cliente_id = ?", 
            (cliente_id,)
        )
        return self.db.cursor.fetchall()

# ... (similar para ClienteCRUD, ServicioCRUD, etc.)