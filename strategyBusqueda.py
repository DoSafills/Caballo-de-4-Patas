from strategy import EstrategiaBusqueda
from models import Admin, Recepcionista, Veterinario, Cliente, Mascota

class BusquedaPorRut(EstrategiaBusqueda):
    def __init__(self, modelo):
        self.modelo = modelo

    def buscar(self, db, rut):
        return db.query(self.modelo).filter_by(rut=rut).first()

class BusquedaPorId(EstrategiaBusqueda):
    def __init__(self, modelo):
        self.modelo = modelo

    def buscar(self, db, id_valor):
        return db.query(self.modelo).filter_by(id=self.obtener_id_campo()).first()

    def obtener_id_campo(self):
        if self.modelo.__name__ == "Cliente":
            return "id_cliente"
        elif self.modelo.__name__ == "Mascota":
            return "id_mascota"
        return "id"  