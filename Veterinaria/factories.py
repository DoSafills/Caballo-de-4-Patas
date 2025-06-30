# factories.py

class VentanaFactory:
    @staticmethod
    def crear(tipo, root, controller):
        if tipo == "gestion":
            from VentanaGestionMascotas import VentanaGestionMascotas
            return VentanaGestionMascotas(root, controller)
        elif tipo == "historial":
            from VentanaHistorialMascota import VentanaHistorialMascota
            return VentanaHistorialMascota(root, controller)
        elif tipo == "principal":
            from Veterinaria import VeterinariaApp
            return VeterinariaApp(root)
        else:
            raise ValueError(f"Tipo de ventana no válido: {tipo}")

# factories.py
class MascotaFactory:
    @staticmethod
    def crear(nombre, raza, sexo, dieta, caracter, habitat, edad, peso, altura, id_vet=None):
        return {
            "nombre": nombre,
            "raza": raza,
            "sexo": sexo,
            "dieta": dieta,
            "caracter": caracter,
            "habitat": habitat,
            "edad": int(edad),
            "peso": peso,
            "altura": altura
        }
