from Persona import Persona

class Cliente(Persona):
    def __init__(self, id_cliente, id_mascota, rut, nombre, apellido):
        super().__init__(rut, nombre, apellido)
        self.id_cliente = id_cliente
        self.id_mascota = id_mascota