# controller.py
import crud

class MascotaController:
    def __init__(self, db, factory):
        self.db = db
        self.factory = factory

    def registrar_mascota(self, datos):
        mascota_data = self.factory.crear(**datos)
        return crud.crear_mascota(self.db, mascota_data)
