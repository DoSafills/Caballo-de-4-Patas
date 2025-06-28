import streamlit as st
from datetime import datetime
from services.mascota_service import listar_mascotas
from services.consulta_service import crear_consulta
from services.usuario_service import listar_usuarios


def mostrar_recepcionista(usuario):
    st.subheader('Agendar Consulta')
    mascotas = listar_mascotas()
    vets = listar_usuarios('veterinario')
    clientes = listar_usuarios('cliente')
    mascota = st.selectbox('Mascota', mascotas, format_func=lambda m: m.nombre)
    vet = st.selectbox('Veterinario', vets, format_func=lambda v: v.nombre)
    cliente = st.selectbox('Cliente', clientes, format_func=lambda c: c.nombre)
    motivo = st.text_input('Motivo')
    fecha = st.date_input('Fecha', datetime.now().date())
    hora = st.time_input('Hora', datetime.now().time())
    if st.button('Agendar'):
        crear_consulta(datetime.combine(fecha, hora), usuario.id_recepcionista, mascota.id_mascota, vet.id_vet, cliente.id_cliente, motivo)
        st.success('Consulta agendada')
