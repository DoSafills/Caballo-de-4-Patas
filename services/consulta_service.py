from datetime import datetime
from database import get_session
from models import Consulta # el models no se deberia usar aca, si no en el repository
from repositories.consulta_repository import ConsultaRepository

def crear_consulta(fecha_hora: datetime, id_recepcionista: int, id_mascota: int, id_vet: int, id_cliente: int, motivo: str):
    with get_session() as db:
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
    with get_session() as db:
        repo = ConsultaRepository(db)
        return repo.get_all()

def obtener_consultas_veterinario(id_vet):
    with get_session() as db:
        return db.query(Consulta).filter_by(id_vet=id_vet).all()