import streamlit as st
from datetime import datetime

from database import get_session
import crud
from models import Admin, Veterinario, Recepcionista, Cliente, Mascota, Consulta


def authenticate(rut: str, password: str):
    """Verifica credenciales y retorna usuario y rol."""
    with get_session() as db:
        for modelo, rol in [
            (Admin, "admin"),
            (Veterinario, "veterinario"),
            (Recepcionista, "recepcionista"),
        ]:
            user = db.query(modelo).filter_by(rut=rut).first()
            if user and user.contrasena == password:
                return user, rol
    return None, None


def admin_view():
    st.header("Administración de usuarios")
    with get_session() as db:
        usuarios = crud.obtener_usuarios_por_tipo(db, "todos")
        data = [
            {"tipo": u.tipo, "rut": u.rut, "nombre": getattr(u, "nombre", "")} 
            for u in usuarios if hasattr(u, "tipo")  # Asegúrate de que solo los usuarios sean procesados
        ]
    st.table(data)


def recepcionista_view(usuario: Recepcionista):
    st.header("Agendar consulta")
    with get_session() as db:
        clientes = db.query(Cliente).all()
        mascotas = db.query(Mascota).all()
        veterinarios = db.query(Veterinario).all()

    cliente = st.selectbox(
        "Cliente", options=clientes, format_func=lambda c: f"{c.id_cliente} - {c.nombre}"
    )
    mascota = st.selectbox(
        "Mascota", options=mascotas, format_func=lambda m: f"{m.id_mascota} - {m.nombre}"
    )
    vet = st.selectbox(
        "Veterinario", options=veterinarios, format_func=lambda v: f"{v.id_vet} - {v.nombre}"
    )
    motivo = st.text_input("Motivo")
    fecha = st.date_input("Fecha")
    hora = st.time_input("Hora")

    if st.button("Agendar"):
        fecha_hora = datetime.combine(fecha, hora)
        with get_session() as db:
            consulta = crud.crear_consulta(
                db,
                fecha_hora,
                usuario.id_recepcionista,
                mascota.id_mascota,
                vet.id_vet,
                cliente.id_cliente,
                motivo,
            )
            if consulta:
                st.success("Consulta agendada correctamente")
            else:
                st.error("No se pudo agendar la consulta")


def veterinario_view(usuario: Veterinario):
    st.header("Consultas asignadas")
    with get_session() as db:
        consultas = db.query(Consulta).filter_by(id_vet=usuario.id_vet).all()
    data = [
        {
            "Fecha": c.fecha_hora,
            "Mascota": c.mascota.nombre,
            "Cliente": c.cliente.nombre,
            "Motivo": c.motivo,
        }
        for c in consultas
    ]
    st.table(data)


def main():
    st.title("Sistema Veterinaria")

    if "usuario" not in st.session_state:
        st.session_state.usuario = None
        st.session_state.rol = None

    if st.session_state.usuario is None:
        rut = st.text_input("RUT")
        password = st.text_input("Contraseña", type="password")
        if st.button("Iniciar sesión"):
            user, rol = authenticate(rut, password)
            if user:
                st.session_state.usuario = user
                st.session_state.rol = rol
                st.rerun()  # Cambié esto de experimental_rerun a rerun
            else:
                st.error("Credenciales inválidas")
        return

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario = None
        st.session_state.rol = None
        st.rerun()  # Cambié esto de experimental_rerun a rerun

    rol = st.session_state.rol
    usuario = st.session_state.usuario

    if rol == "admin":
        admin_view()
    elif rol == "recepcionista":
        recepcionista_view(usuario)
    elif rol == "veterinario":
        veterinario_view(usuario)


if __name__ == "__main__":
    main()
