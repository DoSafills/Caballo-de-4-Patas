import streamlit as st
from services.usuario_service import listar_usuarios, crear_usuario, eliminar_usuario, actualizar_usuario

def mostrar_admin():
    st.title("Gestión de Administradores")

    # Mostrar tabla de admins
    st.subheader("Usuarios Registrados")
    admins = listar_usuarios('admin')

    if admins:
        for admin in admins:
            with st.expander(f"{admin.nombre} ({admin.rut})"):
                col1, col2 = st.columns(2)

                with col1:
                    nuevo_nombre = st.text_input("Nombre", admin.nombre, key=f"nombre_{admin.rut}")
                    nuevo_apellido = st.text_input("Apellido", admin.apellido, key=f"apellido_{admin.rut}")
                    nuevo_email = st.text_input("Email", admin.email or "", key=f"email_{admin.rut}")

                with col2:
                    nueva_edad = st.number_input("Edad", 0, 120, admin.edad or 0, key=f"edad_{admin.rut}")
                    nueva_contra = st.text_input("Contraseña", admin.contrasena, key=f"contra_{admin.rut}")

                col_actualizar, col_eliminar = st.columns(2)

                with col_actualizar:
                    if st.button("Actualizar", key=f"update_{admin.rut}"):
                        nuevos_datos = {
                            "nombre": nuevo_nombre,
                            "apellido": nuevo_apellido,
                            "edad": nueva_edad,
                            "email": nuevo_email,
                            "contrasena": nueva_contra
                        }
                        if actualizar_usuario("admin", admin.rut, nuevos_datos):
                            st.success("Usuario actualizado correctamente.")
                            st.rerun()
                        else:
                            st.error("No se pudo actualizar.")

                with col_eliminar:
                    if st.button("Eliminar", key=f"delete_{admin.rut}"):
                        if eliminar_usuario("admin", admin.rut):
                            st.success("Usuario eliminado correctamente.")
                            st.rerun()
                        else:
                            st.error("No se pudo eliminar.")

    else:
        st.info("No hay administradores registrados.")

    # Formulario para registrar nuevo usuario
    st.subheader("Registrar Nuevo Usuario")

    with st.form("registro_usuario"):
        rut = st.text_input("RUT")
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        edad = st.number_input("Edad", min_value=0, max_value=120)
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        rol = st.selectbox("Rol", ["admin", "veterinario", "recepcionista"])

        # Campos adicionales según rol
        especializacion = ""
        if rol == "veterinario":
            especializacion = st.text_input("Especialización")

        submitted = st.form_submit_button("Registrar")

        if submitted:
            campos_obligatorios = all([rut, nombre, apellido, edad, email, password])

            if campos_obligatorios:
                datos_usuario = {
                    "rut": rut,
                    "nombre": nombre,
                    "apellido": apellido,
                    "edad": edad,
                    "email": email,
                    "contrasena": password
                }

                # Agregar campo adicional solo si es veterinario
                if rol == "veterinario":
                    datos_usuario["especializacion"] = especializacion

                exito = crear_usuario(rol, datos_usuario)

                if exito:
                    st.success(f"Usuario {nombre} ({rol}) registrado exitosamente.")
                    st.rerun()
                else:
                    st.error("Error: El usuario ya existe o los datos son inválidos.")
            else:
                st.warning("Por favor completa todos los campos obligatorios.")
