from Veterinaria.models import Admin, Recepcionista, Veterinario

class FactoriUsuario:
    @staticmethod
    def crear_usuario(tipo, datos):
        if tipo == "admin":
            return Admin(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                tipo="admin",
                contrasena=datos["contrasena"]
            )
        elif tipo == "recepcionista":
            return Recepcionista(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                tipo="recepcionista",
                contrasena=datos["contrasena"]
            )
        elif tipo == "veterinario":
            return Veterinario(
                rut=datos["rut"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                edad=datos["edad"],
                email=datos["email"],
                tipo="veterinario",
                contrasena=datos["contrasena"],
                especializacion=datos["especializacion"]
            )
        else:
            raise ValueError("tipo de usuario no válido")
