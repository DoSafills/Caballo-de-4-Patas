from typing import List
from fpdf import FPDF
from Veterinaria.models import Consulta


def generar_reporte_consultas(consultas: List[Consulta], ruta: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, 'Reporte de Consultas', ln=1)
    for c in consultas:
        linea = f"{c.fecha_hora} - {c.mascota.nombre} - {c.motivo}"
        pdf.cell(0, 10, linea, ln=1)
    pdf.output(ruta)
    return ruta
