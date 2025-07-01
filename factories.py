# factories.py

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
