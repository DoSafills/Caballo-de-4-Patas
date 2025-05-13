from Usuario import Usuario

class Admin(Usuario):
    def __init__(self, id_admin, contrasena, rut, nombre, apellido, edad, email, tipo):
        super().__init__(rut, nombre, apellido, edad, email, tipo)
        self.id_admin = id_admin
        self.contrasena = contrasena