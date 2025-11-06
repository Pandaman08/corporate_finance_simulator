import streamlit as st

def render_home():
    """Renderiza la pantalla de inicio del simulador"""
    
    # Título principal con estilo para tema oscuro
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #FF4B4B; font-size: 3rem; margin-bottom: 0.5rem;'>
                🪙 Simulador de Finanzas Corporativas
            </h1>
            <p style='color: #CCCCCC; font-size: 1.2rem;'>
                Planifica tu futuro financiero con herramientas profesionales
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Descripción del simulador
    st.markdown("""
    ### 🎯 ¿Qué es este simulador?
    
    Una herramienta integral que te permite:
    - 📈 **Proyectar** el crecimiento de tus inversiones
    - 💰 **Calcular** tu pensión de jubilación esperada
    - 📊 **Valorar** bonos e instrumentos de renta fija
    - 📄 **Exportar** reportes profesionales en PDF
    """)
    
    st.markdown("---")
    
    # Módulos disponibles - Con fondos de colores contrastantes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #2D3047; padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid #444; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
            <h3 style='color: #FF6B6B;'>📈 Módulo A</h3>
            <h4 style='color: #FFFFFF;'>Crecimiento de Cartera</h4>
            <p style='font-size: 0.9rem; color: #E0E0E0;'>
                Simula el crecimiento de tu capital con aportes periódicos 
                e interés compuesto. Visualiza tu patrimonio futuro.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #1B4332; padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid #2D6A4F; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
            <h3 style='color: #52B788;'>💰 Módulo B</h3>
            <h4 style='color: #FFFFFF;'>Proyección de Jubilación</h4>
            <p style='font-size: 0.9rem; color: #E0E0E0;'>
                Calcula tu pensión mensual estimada o el monto total 
                disponible al jubilarte. Compara escenarios.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #5C4D00; padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid #FFD700; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
            <h3 style='color: #FFD700;'>📊 Módulo C</h3>
            <h4 style='color: #FFFFFF;'>Valoración de Bonos</h4>
            <p style='font-size: 0.9rem; color: #E0E0E0;'>
                Determina el valor presente de bonos con cupones. 
                Analiza flujos de caja descontados.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Características principales
    st.markdown("### ✨ Características Principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - ✅ **Cálculos precisos** basados en fórmulas financieras validadas
        - 📊 **Gráficas interactivas** para visualizar resultados
        - 💵 **Montos en dólares** (USD) con redondeo a 2 decimales
        - 🔒 **Validaciones** para evitar errores de entrada
        """)
    
    with col2:
        st.markdown("""
        - 📈 **Tasas equivalentes** automáticas entre periodos
        - 💼 **Impuestos** configurables (5% o 29.5%)
        - 📄 **Exportación a PDF** con formato profesional
        - ❓ **Ayuda contextual** en cada campo
        """)
    
    st.markdown("---")
    
    # Instrucciones de uso
    with st.expander("📖 ¿Cómo usar el simulador?", expanded=False):
        st.markdown("""
        ### Pasos para empezar:
        
        1. **Selecciona un módulo** en el menú lateral izquierdo
        2. **Ingresa los datos** solicitados en cada campo
        3. **Presiona el botón** de cálculo correspondiente
        4. **Revisa los resultados** mostrados en pantalla
        5. **Exporta a PDF** si deseas guardar el reporte
        
        ### Flujo recomendado:
        
        1. Comienza con el **Módulo A** para calcular tu capital acumulado
        2. Usa ese resultado en el **Módulo B** para ver tu pensión
        3. Opcionalmente, calcula bonos en el **Módulo C**
        4. Exporta todo a un **PDF profesional**
        
        ### Tips útiles:
        
        - Usa el ícono **?** junto a cada campo para ver ayuda
        - Los resultados se guardan automáticamente entre módulos
        - Puedes modificar los valores y recalcular cuantas veces quieras
        - El PDF incluye gráficas y tablas detalladas
        """)
    
    st.markdown("---")
    
    # Conceptos financieros clave
    with st.expander("💡 Conceptos Financieros Clave", expanded=False):
        st.markdown("""
        ### Glosario de Términos
        
        **TEA (Tasa Efectiva Anual):** Rentabilidad o costo anualizado que incluye 
        capitalización de intereses.
        
        **Interés Compuesto:** Intereses que se calculan sobre el capital inicial 
        más los intereses acumulados.
        
        **Valor Presente (PV):** Valor actual de flujos futuros descontados a una 
        tasa de retorno.
        
        **Tasa Cupón:** Tasa de interés nominal que paga un bono sobre su valor nominal.
        
        **Pensión Mensual:** Pago periódico calculado como anualidad desde un capital inicial.
        
        **Impuesto sobre Ganancias:** Tributo que se aplica solo sobre las utilidades 
        generadas, no sobre el capital inicial.
        """)
    
    st.markdown("---")
    
    # Llamada a la acción con fondo contrastante
    st.markdown("""
    <div style='background-color: #1B4332; padding: 2rem; border-radius: 10px; border: 2px solid #52B788; text-align: center; box-shadow: 0 4px 12px rgba(82, 183, 136, 0.3);'>
        <h3 style='color: #52B788; margin-bottom: 1rem;'>🚀 ¡Comienza ahora!</h3>
        <p style='color: #FFFFFF; font-size: 1.1rem;'>
        Selecciona un módulo en el <strong style='color: #52B788;'>menú lateral</strong> para empezar a simular tu futuro financiero.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Información adicional en pie de página
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.8rem; margin-top: 3rem; padding: 1rem;'>
        <p>Simulador de Finanzas Corporativas v1.0</p>
        <p>Desarrollado como proyecto académico | Los resultados son referenciales</p>
    </div>
    """, unsafe_allow_html=True)