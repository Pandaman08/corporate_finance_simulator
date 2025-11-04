import streamlit as st
import pandas as pd
from src.finance_engine import bond_present_value
from src.utils import validate_inputs

def render_module_c(help_texts):
    st.header("Módulo C — Valoración de bonos")
    
    col1, col2 = st.columns(2)
    with col1:
        face_value = st.number_input(
            "Valor nominal (USD)",
            min_value=0.0, value=1000.0, step=100.0,
            help=help_texts["valor_nominal"]
        )
        coupon_rate = st.number_input(
            "Tasa Cupón (% TEA)",
            min_value=0.0, max_value=100.0, value=5.0, step=0.1,
            help=help_texts["tasa_coupon"]
        )
        payment_freq = st.selectbox(
            "Frecuencia de pago",
            ["Mensual", "Bimestral", "Trimestral", "Cuatrimestral", "Semestral", "Anual"],
            help=help_texts["frecuencia_pago_bono"]
        )
    with col2:
        years_to_maturity = st.number_input(
            "Plazo en años",
            min_value=0.1, max_value=50.0, value=10.0, step=0.5,
            help=help_texts["plazo_bono"]
        )
        required_yield = st.number_input(
            "Tasa de retorno esperada (% TEA)",
            min_value=0.0, max_value=50.0, value=6.0, step=0.1,
            help=help_texts["tasa_retorno_bono"]
        )
    
    if st.button("Calcular valor del bono"):
        errors = validate_inputs(
            face_value=face_value,
            coupon_rate=coupon_rate,
            required_yield=required_yield
        )
        if errors:
            for e in errors:
                st.error(e)
        else:
            df_flows, pv_total = bond_present_value(
                face_value, coupon_rate, payment_freq, years_to_maturity, required_yield
            )
            st.metric("Valor Presente del Bono (USD)", f"${pv_total:,.2f}")
            
            st.subheader("Flujos descontados")
            st.dataframe(df_flows.round(2))
            
            st.session_state['module_c_result'] = {
                'df_flows': df_flows,
                'pv_total': pv_total,
                'face_value': face_value,
                'coupon_rate': coupon_rate,
                'years': years_to_maturity,
                'yield': required_yield
            }