import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from controller import MascotaController
from models import create_tables
from factories import VentanaFactory  # Opcional si usas otras páginas

# FACTORY
class MascotaFactory:
    @staticmethod
    def crear(nombre, raza, sexo, dieta, caracter, habitat, edad, peso, altura, id_vet=None):
        return {
            "nombre": nombre,
            "raza": raza,
            "sexo": sexo,
            "dieta": dieta,
            "caracter": caracter,
            "habitat": habitat,
            "edad": int(edad),
            "peso": peso,
            "altura": altura
        }

# --- Configuración de la DB
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "veterinaria.db")
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
db = Session()

controller = MascotaController(db, MascotaFactory)

# --- UI con Streamlit
st.set_page_config(page_title="Home Pets - Asistencia", layout="centered")

st.title("🐾 HOME PETS")
st.subheader("Asistencia de Reserva")
st.markdown("**Precio de la consulta: CLP $5.000**")
st.markdown("### Paso 4 → Datos")

with st.form("registro_form"):
    st.markdown("#### Datos de la Mascota")

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre", placeholder="Fido")
        raza = st.text_input("Raza", placeholder="Golden")
        peso = st.text_input("Peso (kg)", placeholder="10.5")
        altura = st.text_input("Altura (cm)", placeholder="40")

        sexo = st.radio("Sexo", options=["Macho", "Hembra"])
        edad = st.selectbox("Edad", [f"{i} años" for i in range(1, 21)])

    with col2:
        dieta = st.selectbox("Dieta", ["Normal", "Especial", "Dietética"])
        caracter = st.selectbox("Carácter", ["Tranquilo", "Agresivo", "Juguetón", "Tímido"])
        habitat = st.selectbox("Hábitat", ["Casa", "Patio", "Campo", "Interior", "Exterior"])

    submitted = st.form_submit_button("REGISTRAR")

    if submitted:
        if not all([nombre, raza, sexo, edad, dieta, caracter, habitat, peso, altura]):
            st.error("Todos los campos son obligatorios.")
        else:
            try:
                datos = {
                    "nombre": nombre,
                    "raza": raza,
                    "sexo": sexo,
                    "dieta": dieta,
                    "caracter": caracter,
                    "habitat": habitat,
                    "edad": edad.split()[0],
                    "peso": peso,
                    "altura": altura
                }
                mascota = controller.registrar_mascota(datos)
                st.success(f"Mascota '{mascota.nombre}' registrada correctamente.")
            except Exception as e:
                db.rollback()
                st.error(f"Error al registrar: {e}")
