from typing import List
from utils.pdf_generator import generar_reporte_consultas
from Veterinaria.database import get_session
from Veterinaria.models import Consulta


def exportar_consultas_pdf(ruta: str) -> str:
    with get_session() as db:
        consultas = db.query(Consulta).all()
    return generar_reporte_consultas(consultas, ruta)
