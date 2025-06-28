import streamlit as st
import requests
from controller import MascotaController
from factories import MascotaFactory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Configuración inicial
st.set_page_config(page_title="Veterinaria HOME PETS", layout="wide")

# Inicializar DB
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "veterinaria.db")
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
db = Session()
controller = MascotaController(db, MascotaFactory)

# Navegación
pagina = st.sidebar.selectbox("Ir a:", ["Registrar Mascota", "Gestión", "Historial"])

if pagina == "Registrar Mascota":
    st.title("Asistencia de Reserva - HOME PETS")
    st.markdown("#### Precio de la consulta: CLP $5.000")

    with st.form("form_mascota"):
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

elif pagina == "Gestión":
    st.title("Gestión de Mascotas")
    mascotas = controller.db.query(controller.model_class).all()

    if not mascotas:
        st.info("No hay mascotas registradas.")
    else:
        selected = st.selectbox("Selecciona una mascota para modificar:", mascotas, format_func=lambda x: f"{x.id_mascota} - {x.nombre} ({x.raza})")

        if selected:
            with st.form("modificar_mascota"):
                edad = st.number_input("Edad", min_value=0, value=selected.edad)
                sexo = st.selectbox("Sexo", ["Macho", "Hembra"], index=["Macho", "Hembra"].index(selected.sexo))
                estado = st.selectbox("Estado Médico", ["Alta", "Pendiente atención", "En tratamiento"])
                historial_nuevo = st.text_input("Añadir al historial", placeholder="Ej: Vacunación")
                actualizar = st.form_submit_button("Guardar Cambios")

                if actualizar:
                    try:
                        nuevos_datos = {
                            "edad": int(edad),
                            "sexo": sexo,
                            "estado": estado
                        }
                        controller.actualizar_mascota(selected.id_mascota, nuevos_datos)

                        if historial_nuevo.strip():
                            controller.agregar_historial(selected.id_mascota, historial_nuevo)

                        st.success("Datos actualizados correctamente.")
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

elif pagina == "Historial":
    st.title("Historial de Mascotas")
    mascotas = controller.db.query(controller.model_class).all()

    if not mascotas:
        st.info("No hay mascotas registradas.")
    else:
        selected = st.selectbox("Selecciona una mascota:", mascotas, format_func=lambda x: f"{x.id_mascota} - {x.nombre}")

        if selected:
            st.subheader(f"Historial de {selected.nombre}")
            historial = controller.obtener_historial(selected.id_mascota)

            if not historial:
                st.warning("Esta mascota no tiene historial registrado.")
            else:
                for h in historial:
                    st.markdown(f"- {h.descripcion} ")