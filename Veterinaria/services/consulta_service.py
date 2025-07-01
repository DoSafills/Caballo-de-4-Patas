from datetime import datetime
from Veterinaria.database import get_session
from Veterinaria.repositories.consulta_repository import ConsultaRepository

def crear_consulta(fecha_hora: datetime, id_recepcionista: int, id_mascota: int, id_vet: int, id_cliente: int, motivo: str):
    with next(get_session()) as db:
        repo = ConsultaRepository(db)
        return repo.add(
            fecha_hora=fecha_hora,
            id_recepcionista=id_recepcionista,
            id_mascota=id_mascota,
            id_vet=id_vet,
            id_cliente=id_cliente,
            motivo=motivo,
        )

def listar_consultas():
    with next(get_session()) as db:
        repo = ConsultaRepository(db)
        return repo.get_all()

def listar_por_mascota(id_mascota: int):
    with next(get_session()) as db:
        repo = ConsultaRepository(db)
        return db.query(repo.model).filter_by(id_mascota=id_mascota).all()