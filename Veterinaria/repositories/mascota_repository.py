from sqlalchemy.orm import Session
from Veterinaria.models import Mascota
from .base_repository import BaseRepository

class MascotaRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Mascota)

    def get_by_id(self, id_mascota: int):
        return self.session.query(self.model).filter(self.model.id_mascota == id_mascota).first()
