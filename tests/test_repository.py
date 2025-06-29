import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from repositories.mascota_repository import MascotaRepository
from veterinaria2.database import get_session


def test_agregar_mascota():
    with get_session() as db:
        repo = MascotaRepository(db)
        mascota = repo.add(nombre='Firulais', raza='Mestizo', sexo='M', dieta='', caracter='', habitat='', edad=2, peso='5', altura='20')
        assert mascota.id_mascota is not None
