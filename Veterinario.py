from Persona import Persona

class Veterinario(Persona):
    def __init__(self, id_vet, especializacion, contrasena, rut, nombre, apellido):
        super().__init__(rut, nombre, apellido)
        self.id_vet = id_vet
        self.especializacion = especializacion
        self.contrasena = contrasena