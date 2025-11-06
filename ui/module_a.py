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

    # Sidebar siempre visible con resumen (se actualizará después del cálculo)
    with st.sidebar:
        st.subheader("📌 Resumen de parámetros (en vivo)")
        st.write("Ajusta los parámetros a la derecha y haz clic en **Calcular**.")
        placeholder_initial = st.empty()
        placeholder_years = st.empty()
        placeholder_tea = st.empty()
        placeholder_final = st.empty()

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
        # genera opciones del 0.5% al 50% para multiselección
        tea_options = [f"{x:.1f}%" for x in [i * 0.5 for i in range(1, 101)]]
        # por defecto incluimos la TEA seleccionada
        default_str = f"{tea:.1f}%"
        selected_teas_str = st.multiselect("Tasas a comparar (incluye la principal)",
                                           options=tea_options,
                                           default=[default_str])
        # convierte strings seleccionadas a floats
        selected_teas = sorted(list({float(s.strip("%")) for s in selected_teas_str}))

    # Actualiza resumen en sidebar en vivo
    placeholder_initial.write(f"**Monto inicial:** ${initial_amount:,.2f}")
    placeholder_years.write(f"**Plazo:** {years} años")
    placeholder_tea.write(f"**TEA seleccionada (principal):** {tea:.2f}%")

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
            return

        # Prepare container for results so la interfaz no salte
        results_container = st.container()
        with results_container:
            # Calcula para cada TEA seleccionada (incluye la principal si la añadiste)
            series_results = {}  # {tea_float: (df, final_balance)}
            for r in selected_teas:
                df_r, final_r = calculate_portfolio_growth(
                    initial_amount, periodic_contribution, contribution_freq, years, r
                )
                series_results[r] = (df_r, final_r)

            # mantén referencia al resultado principal (para métricas)
            if tea in series_results:
                df_main, final_balance = series_results[tea]
            else:
                # si el usuario no incluyó la TEA principal en multiselect, calcula y úsala
                df_main, final_balance = calculate_portfolio_growth(
                    initial_amount, periodic_contribution, contribution_freq, years, tea
                )
                series_results[tea] = (df_main, final_balance)

            # --- INDICADORES INTELIGENTES ---
            total_contrib = df_main["Aporte"].sum() + initial_amount
            # ROI relativo a los aportes totales
            roi_percent = ((final_balance / total_contrib) - 1) * 100 if total_contrib != 0 else 0.0
            # CAGR estimado (nota: si hay aportes periódicos, CAGR simple usa initial_amount para referencia)
            cagr = None
            if initial_amount > 0:
                try:
                    cagr = (final_balance / initial_amount) ** (1 / years) - 1
                except Exception:
                    cagr = None

            # Muestra métricas principales
            st.subheader("📊 Resultados del simulador")
            colm1, colm2, colm3 = st.columns(3)
            colm1.metric("Capital acumulado (USD)", f"${final_balance:,.2f}")
            colm2.metric("Aportes totales (USD)", f"${total_contrib:,.2f}")
            colm3.metric("Ganancia (USD)", f"${final_balance - total_contrib:,.2f}")

            colm4, colm5 = st.columns(2)
            colm4.metric("ROI (%)", f"{roi_percent:.2f}%")
            colm5.metric("CAGR aprox. (%)", f"{(cagr * 100):.2f}%" if cagr is not None else "N/A")

            # Actualiza sidebar con resultado final
            placeholder_final.write(f"**Capital final (TEA {tea:.2f}%):** ${final_balance:,.2f}")

            # --- GRÁFICO INTERACTIVO MULTISERIE ---
            st.subheader("📈 Evolución del fondo (interactivo)")
            fig = go.Figure()
            colors = ['#007ACC', '#FFB703', '#FB8500', '#2a9d8f', '#8338ec', '#ff006e']
            for i, r in enumerate(sorted(series_results.keys())):
                df_r, final_r = series_results[r]
                name = f"Saldo Total ({r:.1f}%)"
                fig.add_trace(go.Scatter(
                    x=df_r['Periodo'],
                    y=df_r['Saldo_Final'],
                    mode='lines+markers',
                    name=name,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=4)
                ))
                # solo dibuja aportes acumulados para la TEA principal (mejora legibilidad)
                if r == tea:
                    fig.add_trace(go.Scatter(
                        x=df_r['Periodo'],
                        y=df_r['Aporte'].cumsum() + initial_amount,
                        mode='lines',
                        name='Aportes acumulados',
                        line=dict(color='#444444', width=2, dash='dash')
                    ))

            fig.update_layout(
                title=dict(text='📊 Crecimiento del capital a lo largo del tiempo', x=0.5),
                xaxis_title='Periodo',
                yaxis_title='Saldo (USD)',
                template='plotly_white',
                hovermode='x unified',
                legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
                margin=dict(t=80, b=60, l=60, r=40)
            )
            fig.update_traces(line_simplify=False)
            st.plotly_chart(fig, use_container_width=True)

            # --- EXPLICACIÓN AUTOMÁTICA (resumen en lenguaje natural) ---
            st.subheader("💬 Interpretación rápida")
            growth_pct = ((final_balance / total_contrib) - 1) * 100 if total_contrib != 0 else 0.0
            if growth_pct >= 0:
                st.write(f"Con una TEA del **{tea:.2f}%** y aportes periódicos totales de **${total_contrib:,.2f}**, "
                         f"el capital final sería **${final_balance:,.2f}**, lo que representa un crecimiento de **{growth_pct:.2f}%** "
                         f"en el periodo seleccionado ({years} años).")
            else:
                st.write(f"Con los parámetros actuales obtendrás una pérdida aproximada de **{abs(growth_pct):.2f}%** respecto a los aportes totales.")

            # --- TABLA DE DETALLES PRINCIPAL ---
            with st.expander("🔍 Ver detalles por periodo (TEA principal)"):
                st.dataframe(df_main.round(2))

            # --- EXPORTAR: CSV y Excel ---
            st.subheader("📥 Exportar resultados")
            # CSV
            csv = df_main.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Descargar resultados (CSV)",
                data=csv,
                file_name="simulacion_periodos.csv",
                mime="text/csv"
            )

            # Excel (intenta crear, si falla vuelve a CSV como fallback)
            try:
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_main.to_excel(writer, index=False, sheet_name='Periodos')
                    # agregamos una hoja de resumen
                    summary_df = pd.DataFrame({
                        "Parámetro": ["Monto inicial", "Aporte periódico", "Frecuencia", "Plazo (años)", "TEA (%)", "Capital final", "Aportes totales", "ROI (%)"],
                        "Valor": [f"${initial_amount:,.2f}", f"${periodic_contribution:,.2f}", contribution_freq, years, f"{tea:.2f}%", f"${final_balance:,.2f}", f"${total_contrib:,.2f}", f"{roi_percent:.2f}%"]
                    })
                    summary_df.to_excel(writer, index=False, sheet_name='Resumen')
                buffer.seek(0)
                st.download_button(
                    label="⬇️ Descargar resultados (Excel)",
                    data=buffer,
                    file_name="simulacion_periodos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception:
                # si falla Excel, ocultamos la opción o le decimos que use CSV
                st.info("La exportación a Excel no está disponible en este entorno. Usa CSV en su lugar.")

            # Guarda en sesión para uso posterior (PDF, reportes, etc.)
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

            # --- OPCIONAL: botón para generar un PDF simple (puedo añadirlo si lo deseas) ---
            st.write("")  # separación visual
            st.caption("¿Quieres que también genere un PDF profesional con el gráfico y un resumen? Dímelo y lo agrego.")
    else:
        st.info("Ajusta los parámetros y haz clic en **Calcular** para ver los resultados del simulador.")      