from sqlalchemy.orm import Session
from Veterinaria.models import Mascota
from .base_repository import BaseRepository


class MascotaRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Mascota)
