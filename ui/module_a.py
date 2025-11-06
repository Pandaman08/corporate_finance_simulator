import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
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
            help=help_texts.get("monto_inicial", "")
        )

        periodic_contribution = st.number_input(
            "Aporte periódico (USD)",
            min_value=0.0, value=100.0, step=50.0,
            help=help_texts.get("aporte_periodico", "")
        )

        contribution_freq = st.selectbox(
            "Frecuencia de aportes",
            ["Mensual", "Trimestral", "Semestral", "Anual"],
            help=help_texts.get("frecuencia_aportes", "")
        )

    with col2:
        years = st.slider(
            "Plazo (años)",
            min_value=1, max_value=50, value=20,
            help=help_texts.get("plazo_anios", "")
        )

        tea = st.slider(
            "Tasa Efectiva Anual (TEA %)",
            min_value=0.1, max_value=50.0, value=5.0, step=0.1,
            help=help_texts.get("tea", "")
        )

        st.markdown("**Comparar con varias TEA (opcional):**")

        # --- Opciones TEA ---
        tea_options = [f"{x:.1f}%" for x in [i * 0.5 for i in range(1, 101)]]
        default_str = f"{tea:.1f}%"

        # Asegura que la TEA esté en opciones
        if default_str not in tea_options:
            closest = min(tea_options, key=lambda x: abs(float(x.strip('%')) - tea))
            default_str = closest

        selected_teas_str = st.multiselect(
            "Tasas a comparar (incluye la principal)",
            options=tea_options,
            default=[default_str]
        )

        # Conversión y limpieza
        selected_teas = sorted(list({float(s.strip('%')) for s in selected_teas_str}))

    # --- SIDEBAR --- (resumen en vivo)
    with st.sidebar:
        st.subheader("📊 Resumen actual de parámetros")
        st.markdown(
            f"""
            - 💵 **Monto inicial:** ${initial_amount:,.2f}  
            - 💰 **Aporte periódico:** ${periodic_contribution:,.2f}  
            - 🔁 **Frecuencia:** {contribution_freq}  
            - ⏳ **Plazo:** {years} años  
            - 📈 **TEA principal:** {tea:.2f}%
            - 📊 **TEAs comparadas:** {', '.join([f'{t:.1f}%' for t in selected_teas])}
            """
        )

    # --- CONTENEDOR DE RESULTADOS ---
    results_container = st.container()

    if st.button("🚀 Calcular crecimiento", use_container_width=True):
        with results_container:
            # Validaciones
            errors = validate_module_a(
                initial_amount=initial_amount,
                periodic_contribution=periodic_contribution,
                tea=tea,
                years=years
            )
            if errors:
                for e in errors:
                    st.error(e)
                return

            # --- Cálculos ---
            series_results = {}
            for r in selected_teas:
                df_r, final_r = calculate_portfolio_growth(
                    initial_amount, periodic_contribution, contribution_freq, years, r
                )
                series_results[r] = (df_r, final_r)

            if tea not in series_results:
                df_main, final_balance = calculate_portfolio_growth(
                    initial_amount, periodic_contribution, contribution_freq, years, tea
                )
                series_results[tea] = (df_main, final_balance)
            else:
                df_main, final_balance = series_results[tea]

            total_contrib = df_main["Aporte"].sum() + initial_amount
            roi_percent = ((final_balance / total_contrib) - 1) * 100 if total_contrib else 0
            cagr = (final_balance / initial_amount) ** (1 / years) - 1 if initial_amount > 0 else 0

            # --- MÉTRICAS ---
            st.subheader("📊 Resultados del simulador")
            colm1, colm2, colm3 = st.columns(3)
            colm1.metric("💰 Capital acumulado", f"${final_balance:,.2f}")
            colm2.metric("📥 Aportes totales", f"${total_contrib:,.2f}")
            colm3.metric("📈 Ganancia neta", f"${final_balance - total_contrib:,.2f}")

            colm4, colm5 = st.columns(2)
            colm4.metric("ROI (%)", f"{roi_percent:.2f}%")
            colm5.metric("CAGR aprox. (%)", f"{cagr * 100:.2f}%")

            # --- GRÁFICO INTERACTIVO ---
            st.subheader("📈 Evolución del fondo (interactivo)")

            # ✅ Lista de colores (corregida)
            colors = ["#0074C2", '#FFB703', "#0B7F72", "#740B0B", "#3A008B", "#D63F80", '#06D6A0', '#118AB2']

            fig = go.Figure()

            for i, r in enumerate(sorted(series_results.keys())):
                df_r, final_r = series_results[r]
                color = colors[i % len(colors)]
                fig.add_trace(go.Scatter(
                    x=df_r['Periodo'],
                    y=df_r['Saldo_Final'],
                    mode='lines+markers',
                    name=f"Saldo Total ({r:.1f}%)",
                    line=dict(color=color, width=3),
                    marker=dict(size=4)
                ))

                # Línea de aportes acumulados solo para la TEA principal
                if r == tea:
                    fig.add_trace(go.Scatter(
                        x=df_r['Periodo'],
                        y=df_r['Aporte'].cumsum() + initial_amount,
                        mode='lines',
                        name='Aportes acumulados',
                        line=dict(color="#29E914", width=2, dash='dash')
                    ))

            fig.update_layout(
                title=dict(text='Crecimiento del capital a lo largo del tiempo', x=0.5),
                xaxis_title='Periodo',
                yaxis_title='Saldo (USD)',
                template='plotly_white',
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5),
                margin=dict(t=60, b=60, l=60, r=40)
            )

            st.plotly_chart(fig, use_container_width=True, key=f"chart_{round(tea,1)}")


            # --- INTERPRETACIÓN ---
            st.subheader("💬 Interpretación rápida")
            growth_pct = ((final_balance / total_contrib) - 1) * 100 if total_contrib else 0
            if growth_pct >= 0:
                st.success(
                    f"Con una TEA del **{tea:.2f}%**, el capital crece hasta **${final_balance:,.2f}**, "
                    f"lo que representa un rendimiento del **{growth_pct:.2f}%** en {years} años."
                )
            else:
                st.warning(
                    f"Con los parámetros actuales habría una pérdida del **{abs(growth_pct):.2f}%** respecto a los aportes totales."
                )

            # --- TABLA DETALLE ---
            with st.expander("🔍 Ver detalles por periodo"):
                st.dataframe(df_main.round(2))

            # --- EXPORTAR ---
            st.subheader("📥 Exportar resultados")
            csv = df_main.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name="simulacion_periodos.csv",
                mime="text/csv"
            )

            try:
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_main.to_excel(writer, index=False, sheet_name='Periodos')
                buffer.seek(0)
                st.download_button(
                    label="⬇️ Descargar Excel",
                    data=buffer,
                    file_name="simulacion_periodos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception:
                st.info("La exportación a Excel no está disponible en este entorno.")

            # --- GUARDAR SESIÓN ---
            st.session_state['module_a_result'] = {
                'df': df_main,
                'final_balance': final_balance,
                'initial_amount': initial_amount,
                'years': years,
                'tea': tea,
                'total_contrib': total_contrib,
                'roi_percent': roi_percent,
                'cagr': cagr
            }

    else:
        with results_container:
            st.info("Ajusta los parámetros y haz clic en **Calcular** para ver los resultados.")
