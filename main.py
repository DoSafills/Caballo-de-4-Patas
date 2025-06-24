import streamlit as st
from ui.login_ui import login_form
from ui.admin_ui import mostrar_admin
from ui.recepcionista_ui import mostrar_recepcionista
from ui.veterinario_ui import mostrar_veterinario


def main():
    st.title('C4P - Gestion Veterinaria')
    usuario = st.session_state.get('usuario')
    if not usuario:
        usuario = login_form()
        if usuario:
            st.session_state['usuario'] = usuario
        else:
            return

    if st.sidebar.button('Cerrar sesión'):
        st.session_state.pop('usuario', None)
        st.experimental_rerun()

    tipo = usuario.tipo
    if tipo == 'admin':
        mostrar_admin()
    elif tipo == 'recepcionista':
        mostrar_recepcionista(usuario)
    elif tipo == 'veterinario':
        mostrar_veterinario(usuario)


if __name__ == '__main__':
    main()
