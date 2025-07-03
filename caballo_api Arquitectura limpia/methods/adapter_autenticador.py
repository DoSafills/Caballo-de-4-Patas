from methods.contextStrategy import ContextoBusqueda
from methods.strategyBusqueda import BusquedaPorRut

class AdapterAutenticadorStrategy:
    def __init__(self, modelos_y_roles):
        """
        modelos_y_roles: lista de tuplas (ModeloSQLAlchemy, rol_str)
        """
        self.modelos_y_roles = modelos_y_roles

    def autenticar(self, db, rut: str, contrasena: str):
        for modelo, rol in self.modelos_y_roles:
            estrategia = ContextoBusqueda(BusquedaPorRut(modelo))
            usuario = estrategia.buscar(db, rut)
            if usuario and usuario.contrasena == contrasena:
                return {
                    "rol": rol,
                    "nombre": usuario.nombre,
                    "usuario": usuario
                }
        return None
