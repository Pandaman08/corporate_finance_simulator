import streamlit as st
from src.finance_engine import calculate_monthly_pension
from src.tax_engine import apply_tax
from src.utils import validate_module_b

def render_module_b(help_texts):
    st.header("Módulo B — Proyección de retiro o pensión mensual")
    
    if 'module_a_result' not in st.session_state:
        st.warning("Complete primero el Módulo A para usar sus resultados.")
        return
    
    result_a = st.session_state['module_a_result']
    capital = result_a['final_balance']
    initial_amount = result_a['initial_amount']
    
    st.info(f"Capital disponible al jubilarse: **${capital:,.2f} USD**")
    
    retirement_option = st.radio(
        "Opción de retiro:",
        ("Cobro total", "Pensión mensual")
    )
    
    tax_type = st.selectbox(
        "Tipo de impuesto",
        ["Ninguno", "Bolsa local (5%)", "Fuente extranjera (29.5%)"],
        help=help_texts["tipo_impuesto"]
    )
    
    if retirement_option == "Cobro total":
        tax, net_amount = apply_tax(capital, initial_amount, tax_type)
        st.metric("Monto neto tras impuestos", f"${net_amount:,.2f}")
        if tax > 0:
            st.metric("Impuesto aplicado", f"-${tax:,.2f}")
        st.session_state['module_b_result'] = {
            'tipo': 'cobro_total',
            'bruto': capital,
            'impuesto': tax,
            'neto': net_amount
        }
    
    else:
        col1, col2 = st.columns(2)
        with col1:
            life_expectancy = st.number_input(
                "Años esperados de retiro",
                min_value=1, max_value=40, value=20
            )
        with col2:
            tea_retirement = st.slider(
                "Tasa de retorno durante retiro (TEA %)",
                min_value=0.0, max_value=20.0, value=3.0, step=0.1
            )
        
        errors = validate_module_b(
            tea_retirement=tea_retirement,
            retirement_years=life_expectancy
        )
        if errors:
            for e in errors:
                st.error(e)
        else:
            monthly_pension_gross = calculate_monthly_pension(capital, life_expectancy, tea_retirement)
            # Impuestos se aplican al capital inicial, no a cada pago mensual (según enunciado)
            tax, net_capital = apply_tax(capital, initial_amount, tax_type)
            monthly_pension_net = calculate_monthly_pension(net_capital, life_expectancy, tea_retirement)
            
            st.metric("Pensión mensual estimada (bruto)", f"${monthly_pension_gross:,.2f}")
            st.metric("Pensión mensual estimada (neto)", f"${monthly_pension_net:,.2f}")
            if tax > 0:
                st.metric("Impuesto aplicado al capital", f"-${tax:,.2f}")
            
            st.session_state['module_b_result'] = {
                'tipo': 'pension_mensual',
                'bruto_mensual': monthly_pension_gross,
                'neto_mensual': monthly_pension_net,
                'impuesto': tax,
                'capital_bruto': capital,
                'capital_neto': net_capital
            }