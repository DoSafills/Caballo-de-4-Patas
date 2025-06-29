from typing import List
from utils.pdf_generator import generar_reporte_consultas
from veterinaria2.database import get_session
from veterinaria2.models import Consulta


def exportar_consultas_pdf(ruta: str) -> str:
    with get_session() as db:
        consultas = db.query(Consulta).all()
    return generar_reporte_consultas(consultas, ruta)
