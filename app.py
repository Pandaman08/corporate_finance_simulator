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
        /* Configuración base que funciona en ambos temas */
        .main {
            color: inherit;
        }
        
        /* Sidebar - forzar tema oscuro */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #262730 0%, #1a1a23 100%) !important;
        }
        
        [data-testid="stSidebar"] * {
            color: #FAFAFA !important;
        }
        
        /* Botones principales */
        .stButton>button {
            background-color: #FF4B4B !important;
            color: white !important;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FF6B6B !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
        }
        
        /* Métricas */
        div[data-testid="metric-container"] {
            background-color: #1E1E1E !important;
            border: 1px solid #333 !important;
            padding: 1.5rem !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #CCCCCC !important;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #1E1E1E !important;
            color: #FAFAFA !important;
            border: 1px solid #333 !important;
            border-radius: 5px !important;
        }
        
        /* Inputs */
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            background-color: #1E1E1E !important;
            color: #FAFAFA !important;
            border: 1px solid #444 !important;
        }
        
        /* Sliders */
        .stSlider>div>div>div {
            background-color: #FF4B4B !important;
        }
        
        /* Títulos */
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }
        
        /* Texto general */
        p, span, div:not([class*="st"]) {
            color: #E0E0E0 !important;
        }
        
        /* Botones de descarga */
        .stDownloadButton>button {
            background-color: #00D4AA !important;
            color: #000000 !important;
            font-weight: bold;
        }
        
        /* Ocultar elementos no deseados */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #1E1E1E;
        }
        ::-webkit-scrollbar-thumb {
            background: #FF4B4B;
            border-radius: 4px;
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