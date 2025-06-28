# streamlit_app.py
import streamlit as st
import requests

st.title("Registrar Mascota")

# Formulario para datos de la mascota
with st.form("form_mascota"):
    nombre = st.text_input("Nombre")
    raza = st.text_input("Raza")
    sexo = st.selectbox("Sexo", ["Macho", "Hembra"])
    dieta = st.text_input("Dieta")
    caracter = st.text_input("Carácter")
    habitat = st.text_input("Hábitat")
    edad = st.number_input("Edad", min_value=0, step=1)
    peso = st.text_input("Peso (ej: 30kg)")
    altura = st.text_input("Altura (ej: 60cm)")
    id_vet = st.number_input("ID Veterinario asignado", min_value=1, step=1)
    
    submit = st.form_submit_button("Registrar")

    if submit:
        data = {
            "nombre": nombre,
            "raza": raza,
            "sexo": sexo,
            "dieta": dieta,
            "caracter": caracter,
            "habitat": habitat,
            "edad": edad,
            "peso": peso,
            "altura": altura,
            "id_vet": id_vet
        }

        try:
            response = requests.post("http://127.0.0.1:8000/mascotas", json=data)
            if response.status_code == 200:
                st.success(f"Mascota '{nombre}' registrada con éxito.")
            else:
                st.error(f"Error al registrar mascota: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar con el servidor FastAPI. ¿Está corriendo?")
