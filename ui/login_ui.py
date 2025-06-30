import streamlit as st
from services.auth_service import authenticate  # La lógica de autenticación que tenías en streamlit_app.py

def login_form():
    st.subheader("Iniciar sesión")
    rut = st.text_input("RUT")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        usuario, tipo = authenticate(rut, password)
        if usuario:
            usuario.tipo = tipo  # Necesario para redirigir luego
            return usuario
        else:
            st.error("Credenciales inválidas")
    return None
