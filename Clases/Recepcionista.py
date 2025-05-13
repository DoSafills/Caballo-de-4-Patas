from Usuario import Usuario

class Recepcionista(Usuario):
    def __init__(self, id_recepcionista, contrasena, rut, nombre, apellido, edad, email, tipo):
        super().__init__(rut, nombre, apellido, edad, email, tipo)
        self.id_recepcionista = id_recepcionista
        self.contrasena = contrasena