import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.finance_engine import calculate_portfolio_growth
from src.utils import validate_inputs
import json

def render_module_a(help_texts):
    st.header("Módulo A — Crecimiento de cartera")
    
    col1, col2 = st.columns(2)
    with col1:
        initial_amount = st.number_input(
            "Monto inicial (USD)",
            min_value=0.0, value=1000.0, step=100.0,
            help=help_texts["monto_inicial"]
        )
        periodic_contribution = st.number_input(
            "Aporte periódico (USD)",
            min_value=0.0, value=100.0, step=50.0,
            help=help_texts["aporte_periodico"]
        )
        contribution_freq = st.selectbox(
            "Frecuencia de aportes",
            ["Mensual", "Trimestral", "Semestral", "Anual"],
            help=help_texts["frecuencia_aportes"]
        )
    with col2:
        years = st.number_input(
            "Plazo (años)",
            min_value=1, max_value=50, value=20,
            help=help_texts["plazo_anios"]
        )
        tea = st.slider(
            "Tasa Efectiva Anual (TEA %)",
            min_value=0.0, max_value=50.0, value=5.0, step=0.1,
            help=help_texts["tea"]
        )
    
    if st.button("Calcular crecimiento"):
        errors = validate_inputs(
            initial_amount=initial_amount,
            periodic_contribution=periodic_contribution,
            tea=tea,
            years=years
        )
        if errors:
            for e in errors:
                st.error(e)
        else:
            df, final_balance = calculate_portfolio_growth(
                initial_amount, periodic_contribution, contribution_freq, years, tea
            )
            st.subheader("Resultados")
            st.metric("Capital acumulado (USD)", f"${final_balance:,.2f}")
            
            st.subheader("Evolución del fondo")
            fig, ax = plt.subplots()
            ax.plot(df['Periodo'], df['Saldo_Final'], label='Saldo Total')
            ax.plot(df['Periodo'], df['Saldo_Inicial'] + df['Aporte'].cumsum(), label='Aportes Acumulados')
            ax.set_xlabel('Periodo')
            ax.set_ylabel('USD')
            ax.legend()
            st.pyplot(fig)
            
            with st.expander("Ver detalles por periodo"):
                st.dataframe(df.round(2))
            
            st.session_state['module_a_result'] = {
                'df': df,
                'final_balance': final_balance,
                'initial_amount': initial_amount,
                'years': years,
                'tea': tea
            }