from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class EstrategiaBusqueda(ABC):
    @abstractmethod
    def buscar(self, db: Session, valor):
        pass