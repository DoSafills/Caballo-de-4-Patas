import streamlit as st
from services.usuario_service import listar_usuarios


def login_form():
    st.header('Login')
    rut = st.text_input('RUT')
    password = st.text_input('Contraseña', type='password')
    if st.button('Ingresar'):
        usuarios = listar_usuarios('admin') + listar_usuarios('veterinario') + listar_usuarios('recepcionista')
        for u in usuarios:
            if u.rut == rut and getattr(u, 'contrasena', '') == password:
                return u
        st.error('Credenciales inválidas')
    return None
