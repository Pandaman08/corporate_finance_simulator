import streamlit as st

def render_sidebar():
    """Renderiza la barra lateral con navegación y opciones"""
    
    # Logo/Título de la aplicación
    st.sidebar.markdown("""
        <div style='text-align: center; padding: 1rem 0; background-color: #1f4788; border-radius: 10px; margin-bottom: 1.5rem;'>
            <h2 style='color: white; margin: 0; font-size: 1.3rem;'>🪙 Finanzas</h2>
            <p style='color: #e8f0fe; margin: 0; font-size: 0.8rem;'>Simulador Corporativo</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Navegación principal
    st.sidebar.markdown("### 📍 Navegación")
    
    module = st.sidebar.radio(
        "Selecciona una opción:",
        (
            "🏠 Inicio",
            "📈 Módulo A — Crecimiento de cartera", 
            "💰 Módulo B — Proyección de retiro", 
            "📊 Módulo C — Valoración de bonos"
        ),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Información de estado
    if 'module_a_result' in st.session_state:
        st.sidebar.success("✅ Módulo A completado")
        capital = st.session_state['module_a_result']['final_balance']
        st.sidebar.info(f"💵 Capital: ${capital:,.2f}")
    
    if 'module_b_result' in st.session_state:
        st.sidebar.success("✅ Módulo B completado")
    
    if 'module_c_result' in st.session_state:
        st.sidebar.success("✅ Módulo C completado")
    
    st.sidebar.markdown("---")
    
    # Acciones rápidas
    st.sidebar.markdown("### ⚡ Acciones Rápidas")
    
    if st.sidebar.button("🔄 Limpiar todos los datos"):
        # Limpiar session state
        keys_to_clear = ['module_a_result', 'module_b_result', 'module_c_result']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.sidebar.success("✅ Datos limpiados")
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Información adicional
    with st.sidebar.expander("ℹ️ Acerca de"):
        st.markdown("""
        **Simulador de Finanzas Corporativas**
        
        Versión 1.0
        
        Herramienta para:
        - Proyección de inversiones
        - Cálculo de pensiones
        - Valoración de bonos
        
        Desarrollado con Python y Streamlit
        """)
    
    return module
