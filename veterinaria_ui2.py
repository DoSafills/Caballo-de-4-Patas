import streamlit as st
from controller import MascotaController
from Veterinaria.factories import MascotaFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import streamlit as st
import requests

# Configuración inicial
st.set_page_config(page_title="Veterinaria HOME PETS", layout="wide")

# URL de la API FastAPI
API_URL = "http://localhost:8000"  # Cambia esto si usas otro puerto o deploy

# Navegación
pagina = st.sidebar.selectbox("Ir a:", ["Registrar Mascota", "Gestión", "Historial"])

if pagina == "Registrar Mascota":
    st.title("Asistencia de Reserva - HOME PETS")
    st.markdown("#### Precio de la consulta: CLP $5.000")

    with st.form("registro_form"):
        st.subheader("Datos de la Mascota")

        nombre = st.text_input("Nombre", placeholder="Fido")
        raza = st.text_input("Raza", placeholder="Golden")
        sexo = st.radio("Sexo", ["Macho", "Hembra"])
        edad = st.selectbox("Edad", [f"{i} años" for i in range(1, 21)])

        dieta = st.selectbox("Dieta", ["Normal", "Especial", "Dietética"])
        caracter = st.selectbox("Carácter", ["Tranquilo", "Agresivo", "Juguetón", "Tímido"])
        habitat = st.selectbox("Hábitat", ["Casa", "Patio", "Campo", "Interior", "Exterior"])

        peso = st.text_input("Peso (kg)", placeholder="10.5")
        altura = st.text_input("Altura (cm)", placeholder="40")

        submit = st.form_submit_button("Registrar")

        if submit:
            if not all([nombre, raza, sexo, edad, dieta, caracter, habitat, peso, altura]):
                st.error("Todos los campos son obligatorios.")
            else:
                try:
                    datos = {
                        "nombre": nombre,
                        "raza": raza,
                        "sexo": sexo,
                        "edad": int(edad.split()[0]),
                        "dieta": dieta,
                        "caracter": caracter,
                        "habitat": habitat,
                        "peso": float(peso),
                        "altura": float(altura)
                    }
                    response = requests.post(f"{API_URL}/mascotas", json=datos)
                    if response.status_code == 201:
                        st.success(f"Mascota '{nombre}' registrada correctamente.")
                    else:
                        st.error(f"Error al registrar mascota: {response.text}")
                except Exception as e:
                    st.error(f"Excepción: {str(e)}")

elif pagina == "Gestión":
    st.title("Gestión de Mascotas")
    mascotas = requests.get(f"{API_URL}/mascotas").json()

    if not mascotas:
        st.info("No hay mascotas registradas.")
    else:
        opciones = [f"{m['id_mascota']} - {m['nombre']} ({m['raza']})" for m in mascotas]
        seleccion = st.selectbox("Selecciona una mascota para modificar:", opciones)
        id_mascota = int(seleccion.split(" - ")[0])
        selected = next((m for m in mascotas if m['id_mascota'] == id_mascota), None)

        if selected:
            with st.form("modificar_mascota"):
                edad = st.number_input("Edad", min_value=0, value=selected["edad"])

                sexo_opciones = ["Macho", "Hembra"]
                sexo = st.selectbox("Sexo", sexo_opciones, index=sexo_opciones.index(selected["sexo"]) if selected["sexo"] in sexo_opciones else 0)

                estado = st.selectbox("Estado Médico", ["Alta", "Pendiente atención", "En tratamiento"])
                historial_nuevo = st.text_input("Añadir al historial", placeholder="Ej: Vacunación")
                actualizar = st.form_submit_button("Guardar Cambios")

                if actualizar:
                    nuevos_datos = {
                        "edad": int(edad),
                        "sexo": sexo,
                        "estado": estado
                    }
                    r = requests.put(f"{API_URL}/mascotas/{id_mascota}", json=nuevos_datos)

                    if r.status_code == 200:
                        if historial_nuevo.strip():
                            h = requests.post(f"{API_URL}/mascotas/{id_mascota}/historial", json={"descripcion": historial_nuevo})
                        st.success("Datos actualizados correctamente.")
                    else:
                        st.error(f"Error al actualizar mascota: {r.text}")

elif pagina == "Historial":
    st.title("Historial de Mascotas")
    mascotas = requests.get(f"{API_URL}/mascotas").json()

    if not mascotas:
        st.info("No hay mascotas registradas.")
    else:
        opciones = [f"{m['id_mascota']} - {m['nombre']}" for m in mascotas]
        seleccion = st.selectbox("Selecciona una mascota:", opciones)
        id_mascota = int(seleccion.split(" - ")[0])
        selected = next((m for m in mascotas if m['id_mascota'] == id_mascota), None)

        if selected:
            st.subheader(f"Historial de {selected['nombre']}")
            historial = requests.get(f"{API_URL}/mascotas/{id_mascota}/historial").json()

            if not historial:
                st.warning("Esta mascota no tiene historial registrado.")
            else:
                for h in historial:
                    st.markdown(f"- {h['descripcion']}")