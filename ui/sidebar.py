import streamlit as st

def render_sidebar():
    st.sidebar.title("Navegación")
    module = st.sidebar.radio(
        "Seleccionar módulo:",
        ("Módulo A — Crecimiento de cartera", 
         "Módulo B — Proyección de retiro", 
         "Módulo C — Valoración de bonos")
    )
    return module