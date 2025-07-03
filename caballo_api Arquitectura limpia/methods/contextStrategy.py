from methods.strategy import EstrategiaBusqueda
class ContextoBusqueda:
    def __init__(self, estrategia: EstrategiaBusqueda):
        self.estrategia = estrategia

    def buscar(self, db, valor):
        return self.estrategia.buscar(db, valor)