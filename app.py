import streamlit as st
from ui.sidebar import render_sidebar
from ui.module_a import render_module_a
from ui.module_b import render_module_b
from ui.module_c import render_module_c
import json
import os
from src.exporters import export_to_pdf

# Configuración inicial
st.set_page_config(page_title="Simulador Finanzas Corporativas", layout="wide")

# Cargar textos de ayuda
with open("assets/help_texts.json", encoding="utf-8") as f:
    help_texts = json.load(f)

# Renderizar barra lateral
selected_module = render_sidebar()

# Renderizar módulo seleccionado
if selected_module.startswith("Módulo A"):
    render_module_a(help_texts)
elif selected_module.startswith("Módulo B"):
    render_module_b(help_texts)
elif selected_module.startswith("Módulo C"):
    render_module_c(help_texts)

# Exportación a PDF (disponible si hay resultados)
if st.sidebar.button("Exportar resultados a PDF"):
    results = {}
    if 'module_a_result' in st.session_state:
        results["Módulo A - Crecimiento"] = {
            'Capital final': st.session_state['module_a_result']['final_balance']
        }
    if 'module_b_result' in st.session_state:
        res = st.session_state['module_b_result']
        if res['tipo'] == 'cobro_total':
            results["Módulo B - Retiro"] = {
                'Tipo': 'Cobro total',
                'Bruto': res['bruto'],
                'Neto': res['neto']
            }
        else:
            results["Módulo B - Retiro"] = {
                'Tipo': 'Pensión mensual',
                'Bruto mensual': res['bruto_mensual'],
                'Neto mensual': res['neto_mensual']
            }
    if 'module_c_result' in st.session_state:
        results["Módulo C - Bono"] = {
            'Valor Presente': st.session_state['module_c_result']['pv_total']
        }
    
    if results:
        export_to_pdf(results, "resultados_finanzas.pdf")
        with open("resultados_finanzas.pdf", "rb") as f:
            st.sidebar.download_button(
                label="Descargar PDF",
                data=f,
                file_name="resultados_finanzas.pdf",
                mime="application/pdf"
            )
    else:
        st.sidebar.warning("No hay resultados para exportar.")