import streamlit as st
from ui.sidebar import render_sidebar
from ui.home import render_home
from ui.module_a import render_module_a
from ui.module_b import render_module_b
from ui.module_c import render_module_c
import json
import os
from src.exporters import export_to_pdf
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="Simulador Finanzas Corporativas",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ==== Corrección de color de texto para ambos temas ==== */

/* Estilo base del texto dentro de contenedores de módulos */
div[data-testid="stHorizontalBlock"] div {
    color: inherit !important;
}

/* Forzar texto claro u oscuro según el tema */
html[data-theme="light"], [data-theme="light"] div[data-testid="stHorizontalBlock"] div {
    color: #222222 !important;  /* Texto oscuro en tema claro */
}

html[data-theme="dark"], [data-theme="dark"] div[data-testid="stHorizontalBlock"] div {
    color: #f2f2f2 !important;  /* Texto claro en tema oscuro */
}

/* Asegurar que los encabezados también cambien */
[data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3, [data-theme="dark"] h4, [data-theme="dark"] h5, [data-theme="dark"] p {
    color: #f2f2f2 !important;
}
[data-theme="light"] h1, [data-theme="light"] h2, [data-theme="light"] h3, [data-theme="light"] h4, [data-theme="light"] h5, [data-theme="light"] p {
    color: #222222 !important;
}
</style>
""", unsafe_allow_html=True)



# Cargar textos de ayuda
try:
    with open("assets/help_texts.json", encoding="utf-8") as f:
        help_texts = json.load(f)
except FileNotFoundError:
    help_texts = {}
    st.warning("No se encontró el archivo de textos de ayuda")

# Renderizar barra lateral
selected_module = render_sidebar()

# Renderizar módulo seleccionado
if selected_module.startswith("🏠"):
    render_home()
elif selected_module.startswith("📈"):
    render_module_a(help_texts)
elif selected_module.startswith("💰"):
    render_module_b(help_texts)
elif selected_module.startswith("📊"):
    render_module_c(help_texts)

# Sección de exportación a PDF en el sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 Exportar Resultados")

# Verificar si hay resultados para exportar
has_results = any([
    'module_a_result' in st.session_state,
    'module_b_result' in st.session_state,
    'module_c_result' in st.session_state
])

if has_results:
    if st.sidebar.button("📥 Generar PDF", key="export_pdf_button"):
        try:
            # Preparar los resultados para exportar
            results = {}
            
            if 'module_a_result' in st.session_state:
                results['module_a_result'] = st.session_state['module_a_result']
            
            if 'module_b_result' in st.session_state:
                results['module_b_result'] = st.session_state['module_b_result']
            
            if 'module_c_result' in st.session_state:
                results['module_c_result'] = st.session_state['module_c_result']
            
            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_finanzas_{timestamp}.pdf"
            
            # Crear el PDF
            with st.spinner("Generando PDF profesional..."):
                export_to_pdf(results, filename)
            
            # Ofrecer descarga
            with open(filename, "rb") as f:
                pdf_data = f.read()
                st.sidebar.download_button(
                    label="⬇️ Descargar PDF",
                    data=pdf_data,
                    file_name=filename,
                    mime="application/pdf",
                    key="download_pdf_button"
                )
            
            st.sidebar.success("✅ PDF generado exitosamente")
            
            # Limpiar archivo temporal después de un tiempo
            try:
                os.remove(filename)
            except:
                pass
                
        except Exception as e:
            st.sidebar.error(f"❌ Error al generar PDF: {str(e)}")
else:
    st.sidebar.info("💡 Completa al menos un módulo para exportar resultados")

# Footer informativo
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='text-align: center; font-size: 0.7rem; color: #888;'>
        <p>Simulador v1.0</p>
        <p>© 2025 Proyecto Académico</p>
    </div>
""", unsafe_allow_html=True)