import streamlit as st
from services.usuario_service import listar_usuarios


def mostrar_admin():
    st.subheader('Usuarios Registrados')
    admins = listar_usuarios('admin')
    data = [{'rut': a.rut, 'nombre': a.nombre} for a in admins]
    st.table(data)
