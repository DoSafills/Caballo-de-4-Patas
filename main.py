import streamlit as st
from ui.login_ui import login_form
from ui.admin_ui import mostrar_admin
from ui.recepcionista_ui import mostrar_recepcionista
from ui.veterinario_ui import mostrar_veterinario

def main():
    st.title('C4P - Gestión Veterinaria')

    # Si no hay usuario autenticado, mostrar formulario login
    if 'usuario' not in st.session_state or st.session_state['usuario'] is None:
        usuario = login_form()
        if usuario:
            st.session_state['usuario'] = usuario
            st.rerun()  # Redirecciona tras login
        return

    # Cerrar sesión
    if st.sidebar.button('Cerrar sesión'):
        st.session_state['usuario'] = None
        st.rerun()

    # Redireccionar según tipo
    usuario = st.session_state['usuario']
    tipo = getattr(usuario, 'tipo', None)

    if tipo == 'admin':
        mostrar_admin()
    elif tipo == 'recepcionista':
        mostrar_recepcionista(usuario)
    elif tipo == 'veterinario':
        mostrar_veterinario(usuario)
    else:
        st.error("Tipo de usuario desconocido")

if __name__ == '__main__':
    main()
