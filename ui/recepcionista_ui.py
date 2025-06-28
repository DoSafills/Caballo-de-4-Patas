import streamlit as st
from datetime import datetime
from services.mascota_service import listar_mascotas, crear_mascota
from services.consulta_service import crear_consulta, listar_consultas
from services.usuario_service import listar_usuarios, crear_usuario


def mostrar_recepcionista(usuario):
    """Vista principal para usuarios recepcionistas."""
    st.subheader('Panel de Recepcionista')

    tabs = st.tabs([
        'Registrar Cliente',
        'Registrar Mascota',
        'Agendar Consulta',
        'Ver Consultas'
    ])

    # --- Registrar Cliente ---
    with tabs[0]:
        st.header('Nuevo Cliente')
        rut = st.text_input('RUT', key='cli_rut')
        nombre = st.text_input('Nombre', key='cli_nombre')
        apellido = st.text_input('Apellido', key='cli_apellido')
        edad = st.number_input('Edad', min_value=0, step=1, key='cli_edad')
        email = st.text_input('Email', key='cli_email')
        if st.button('Guardar Cliente'):
            crear_usuario('cliente', {
                'rut': rut,
                'nombre': nombre,
                'apellido': apellido,
                'edad': edad,
                'email': email
            })
            st.success('Cliente registrado')

    # --- Registrar Mascota ---
    with tabs[1]:
        st.header('Nueva Mascota')
        clientes = listar_usuarios('cliente')
        veterinarios = listar_usuarios('veterinario')
        cliente = st.selectbox('Cliente', clientes, format_func=lambda c: c.nombre, key='masc_cliente')
        vet = st.selectbox('Veterinario', veterinarios, format_func=lambda v: v.nombre, key='masc_vet')
        nombre = st.text_input('Nombre Mascota', key='masc_nombre')
        raza = st.text_input('Raza', key='masc_raza')
        sexo = st.text_input('Sexo', key='masc_sexo')
        edad = st.number_input('Edad Mascota', min_value=0, step=1, key='masc_edad')
        peso = st.text_input('Peso', key='masc_peso')
        altura = st.text_input('Altura', key='masc_altura')
        dieta = st.text_input('Dieta', key='masc_dieta')
        caracter = st.text_input('Carácter', key='masc_caracter')
        habitat = st.text_input('Hábitat', key='masc_habitat')
        if st.button('Guardar Mascota'):
            crear_mascota(
                nombre=nombre,
                raza=raza,
                sexo=sexo,
                dieta=dieta,
                caracter=caracter,
                habitat=habitat,
                id_vet=vet.id_vet,
                edad=edad,
                peso=peso,
                altura=altura,
                id_cliente=cliente.id_cliente
            )
            st.success('Mascota registrada')

    # --- Agendar Consulta ---
    with tabs[2]:
        st.header('Agendar Consulta')
        mascotas = listar_mascotas()
        vets = listar_usuarios('veterinario')
        clientes = listar_usuarios('cliente')
        mascota = st.selectbox('Mascota', mascotas, format_func=lambda m: m.nombre, key='cons_mascota')
        vet = st.selectbox('Veterinario', vets, format_func=lambda v: v.nombre, key='cons_vet')
        cliente = st.selectbox('Cliente', clientes, format_func=lambda c: c.nombre, key='cons_cliente')
        motivo = st.text_input('Motivo', key='cons_motivo')
        fecha = st.date_input('Fecha', datetime.now().date(), key='cons_fecha')
        hora = st.time_input('Hora', datetime.now().time(), key='cons_hora')
        if st.button('Agendar Consulta'):
            crear_consulta(
                datetime.combine(fecha, hora),
                usuario.id_recepcionista,
                mascota.id_mascota,
                vet.id_vet,
                cliente.id_cliente,
                motivo
            )
            st.success('Consulta agendada')

    # --- Ver Consultas ---
    with tabs[3]:
        st.header('Consultas Agendadas')
        consultas = listar_consultas()
        data = [
            {
                'Fecha': c.fecha_hora,
                'Mascota': c.mascota.nombre,
                'Cliente': c.cliente.nombre,
                'Veterinario': c.veterinario.nombre,
                'Motivo': c.motivo
            }
            for c in consultas
        ]
        st.table(data)

    if st.button('Cerrar sesión'):
        st.session_state.pop('usuario', None)
        st.experimental_rerun()
