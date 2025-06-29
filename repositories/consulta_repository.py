from sqlalchemy.orm import Session
from Veterinaria.models import Consulta
from .base_repository import BaseRepository


class ConsultaRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Consulta)
