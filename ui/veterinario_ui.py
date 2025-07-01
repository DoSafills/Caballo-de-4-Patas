import streamlit as st
from database import get_session
from models import Cliente
from services.consulta_service import obtener_consultas_veterinario
from services.mascota_service import registrar_mascota

def mostrar_veterinario(veterinario):
    st.title(f"Panel Veterinario - Dr. {veterinario.nombre}")

    # Sección: Consultas asignadas
    st.subheader("Consultas asignadas")
    consultas = obtener_consultas_veterinario(veterinario.id_vet)

    if not consultas:
        st.info("No tienes consultas asignadas.")
    else:
        for c in consultas:
            st.markdown("---")
            st.markdown(f"### 🐾 Mascota: {c.mascota.nombre}")
            st.markdown(f"**Fecha y hora:** {c.fecha_hora}")
            st.markdown(f"**Motivo:** {c.motivo}")
            st.markdown(f"**Cliente:** {c.cliente.nombre}")

    # Sección: Formulario para registrar mascota
    st.subheader("Registrar nueva mascota")
    formulario_registrar_mascota_para_veterinario(veterinario)


def formulario_registrar_mascota_para_veterinario(veterinario):
    with get_session() as db:
        clientes = db.query(Cliente).all()

    if not clientes:
        st.warning("No hay clientes registrados en el sistema.")
        return

    cliente = st.selectbox("Cliente", clientes, format_func=lambda c: f"{c.id_cliente} - {c.nombre}")

    with st.form("form_mascota_vet"):
        nombre = st.text_input("Nombre")
        raza = st.text_input("Raza")
        sexo = st.selectbox("Sexo", ["Macho", "Hembra"])
        dieta = st.text_input("Dieta")
        caracter = st.text_input("Carácter")
        habitat = st.text_input("Hábitat")
        edad = st.number_input("Edad", min_value=0)
        peso = st.text_input("Peso (ej: 30kg)")
        altura = st.text_input("Altura (ej: 60cm)")
        estado = st.selectbox("Estado de salud", ["saludable", "en tratamiento", "crítico"])

        enviar = st.form_submit_button("Registrar")

        if enviar:
            if not nombre or not raza or not peso or not altura:
                st.error("Por favor, completa todos los campos obligatorios.")
                return

            datos = {
                "nombre": nombre,
                "raza": raza,
                "sexo": sexo,
                "dieta": dieta,
                "caracter": caracter,
                "habitat": habitat,
                "edad": edad,
                "peso": peso,
                "altura": altura,
                "estado": estado,
                "id_vet": veterinario.id_vet,
                "id_cliente": cliente.id_cliente
            }

            exito = registrar_mascota(datos)
            if exito:
                st.success(f"Mascota '{nombre}' registrada correctamente.")
            else:
                st.error("No se pudo registrar la mascota.")
