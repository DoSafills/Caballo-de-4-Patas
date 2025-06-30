import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Veterinaria HOME PETS", layout="wide")

pagina = st.sidebar.selectbox("Ir a:", ["Registrar Mascota", "Gestión", "Historial"])

if pagina == "Registrar Mascota":
    st.title("Asistencia de Reserva - HOME PETS")
    st.markdown("#### Precio de la consulta: CLP $5.000")

    with st.form("form_mascota"):
        st.subheader("Datos de la Mascota")

        nombre = st.text_input("Nombre", placeholder="Fido")
        raza = st.text_input("Raza", placeholder="Golden")
        sexo = st.radio("Sexo", ["Macho", "Hembra"])
        edad = st.selectbox("Edad", [i for i in range(1, 21)])

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
                response = requests.post(f"{API_URL}/mascotas", json=data)
                if response.status_code == 200:
                    st.success(f"Mascota '{nombre}' registrada con éxito.")
                else:
                    st.error(f"Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("No se pudo conectar con el servidor FastAPI.")

elif pagina == "Gestión":
    st.title("Gestión de Mascotas")
    try:
        response = requests.get(f"{API_URL}/mascotas")
        mascotas = response.json() if response.status_code == 200 else []
    except:
        st.error("Error de conexión con el API.")
        mascotas = []

    if not mascotas:
        st.info("No hay mascotas registradas.")
    else:
        selected = st.selectbox("Selecciona una mascota:", mascotas,
                                format_func=lambda x: f"{x['id_mascota']} - {x['nombre']} ({x['raza']})")

        if selected:
            with st.form("modificar_mascota"):
                edad = st.number_input("Edad", min_value=0, value=selected['edad'])

                opciones_sexo = ["Macho", "Hembra"]
                sexo_valor = selected.get('sexo', 'Macho')  # valor por defecto

                # Asegurarse de que el sexo esté en las opciones
                if sexo_valor not in opciones_sexo:
                    sexo_index = 0  # Por ejemplo, Macho como predeterminado
                else:
                    sexo_index = opciones_sexo.index(sexo_valor)

                sexo = st.selectbox("Sexo", opciones_sexo, index=sexo_index)

                estado = st.selectbox("Estado Médico", ["Alta", "Pendiente atención", "En tratamiento"],
                                    index=["Alta", "Pendiente atención", "En tratamiento"].index(selected.get("estado", "Pendiente atención")))
                historial_nuevo = st.text_input("Añadir al historial", placeholder="Ej: Vacunación")
                actualizar = st.form_submit_button("Guardar Cambios")

                if actualizar:
                    try:
                        data = {
                            "edad": edad,
                            "sexo": sexo,
                            "estado": estado
                        }
                        res = requests.put(f"{API_URL}/mascotas/{selected['id_mascota']}", json=data)

                        # Depuracion
                        st.write("Código de respuesta:", res.status_code)
                        st.write("Mensaje de respuesta:", res.text)
                        st.write("Datos enviados:", data)
                        st.write("URL usada:", f"{API_URL}/mascotas/{selected['id_mascota']}")

                        if historial_nuevo.strip():
                            historial_data = {
                                "id_mascota": selected['id_mascota'],
                                "id_vet": selected['id_vet'],  # Se espera que venga de la mascota
                                "id_cliente": 1,  # Ajustar según sea necesario
                                "id_recepcionista": 1,  # Ajustar según sea necesario
                                "motivo": historial_nuevo,
                                "fecha_hora": "2025-01-01T00:00:00"  # Agregar fecha real si se desea
                            }
                            requests.post(f"{API_URL}/historial", json=historial_data)

                        if res.status_code == 200:
                            st.success("Datos actualizados correctamente.")
                        else:
                            st.error("Error al actualizar mascota.")
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

elif pagina == "Historial":
    st.title("Historial de Mascotas")
    try:
        response = requests.get(f"{API_URL}/mascotas")
        mascotas = response.json() if response.status_code == 200 else []
    except:
        st.error("No se pudo obtener la lista de mascotas.")
        mascotas = []

    if not mascotas:
        st.info("No hay mascotas registradas.")
    else:
        selected = st.selectbox("Selecciona una mascota:", mascotas,
                                format_func=lambda x: f"{x['id_mascota']} - {x['nombre']}")

        if selected:
            try:
                response = requests.get(f"{API_URL}/historial/{selected['id_mascota']}")
                historial = response.json() if response.status_code == 200 else []
            except:
                historial = []

            st.subheader(f"Historial de {selected['nombre']}")
            if not historial:
                st.warning("Esta mascota no tiene historial registrado.")
            else:
                for h in historial:
                    st.markdown(f"- {h['motivo']} ({h['fecha_hora']})")
