import streamlit as st
from services.consulta_service import listar_consultas


def mostrar_veterinario(usuario):
    st.subheader('Consultas Asignadas')
    consultas = [c for c in listar_consultas() if c.id_vet == usuario.id_vet]
    data = [
        {
            'fecha': c.fecha_hora,
            'mascota': c.mascota.nombre,
            'motivo': c.motivo
        } for c in consultas
    ]
    st.table(data)
