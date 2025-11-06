import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.finance_engine import calculate_portfolio_growth
from src.utils import validate_module_a
import json

def render_module_a(help_texts):
    st.header("💰 Módulo A — Simulador de Crecimiento de Cartera")
    st.caption("Simula cómo crecería tu inversión con diferentes tasas, plazos y aportes periódicos.")

    # --- ENTRADAS ---
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
        years = st.slider(
            "Plazo (años)",
            min_value=1, max_value=50, value=20,
            help=help_texts["plazo_anios"]
        )
        tea = st.slider(
            "Tasa Efectiva Anual (TEA %)",
            min_value=0.1, max_value=50.0, value=5.0, step=0.1,
            help=help_texts["tea"]
        )
        compare = st.checkbox("Comparar con otra TEA", help="Activa para comparar una segunda tasa de rendimiento.")
        if compare:
            tea_alt = st.slider(
                "TEA alternativa (%)", min_value=0.1, max_value=50.0, value=7.0, step=0.1,
                help="Permite comparar otra tasa efectiva anual."
            )
        else:
            tea_alt = None

    # --- BOTÓN DE CÁLCULO ---
    if st.button("🚀 Calcular crecimiento"):
        errors = validate_module_a(
            initial_amount=initial_amount,
            periodic_contribution=periodic_contribution,
            tea=tea,
            years=years
        )

        if errors:
            for e in errors:
                st.error(e)
        else:
            # Cálculo principal
            df, final_balance = calculate_portfolio_growth(
                initial_amount, periodic_contribution, contribution_freq, years, tea
            )

            # --- RESULTADOS PRINCIPALES ---
            st.subheader("📊 Resultados del simulador")
            total_contrib = df["Aporte"].sum() + initial_amount
            st.metric("Capital acumulado (USD)", f"${final_balance:,.2f}")
            st.metric("Aportes totales", f"${total_contrib:,.2f}")
            st.metric("Ganancia obtenida", f"${final_balance - total_contrib:,.2f}")

            # --- COMPARACIÓN OPCIONAL ---
            if tea_alt:
                df_alt, final_alt = calculate_portfolio_growth(
                    initial_amount, periodic_contribution, contribution_freq, years, tea_alt
                )
                st.info(f"Con una TEA del {tea_alt:.2f}% obtendrías un capital final de **${final_alt:,.2f}**")

            # --- GRÁFICO MEJORADO ---
            st.subheader("📈 Evolución del fondo")
            fig, ax = plt.subplots(figsize=(10, 4))

            ax.plot(df['Periodo'], df['Saldo_Final'], label=f'Saldo Total ({tea:.1f}%)', color='#007ACC', linewidth=2)
            ax.plot(df['Periodo'], df['Aporte'].cumsum() + initial_amount,
                    label='Aportes acumulados', linestyle='--', color='#FFB703', linewidth=2)

            if tea_alt:
                ax.plot(df_alt['Periodo'], df_alt['Saldo_Final'],
                        label=f'Saldo Alternativo ({tea_alt:.1f}%)', color='#FB8500', linewidth=2)

            ax.set_xlabel('Periodo', fontsize=11)
            ax.set_ylabel('Saldo (USD)', fontsize=11)
            ax.set_title('Crecimiento del capital a lo largo del tiempo', fontsize=13, fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
            st.pyplot(fig)

            # --- TABLA DE DETALLES ---
            with st.expander("🔍 Ver detalles por periodo"):
                st.dataframe(df.round(2))

            # --- GUARDAR EN SESIÓN ---
            st.session_state['module_a_result'] = {
                'df': df,
                'final_balance': final_balance,
                'initial_amount': initial_amount,
                'years': years,
                'tea': tea
            }
