import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.finance_engine import bond_present_value
from src.utils import validate_module_c

def render_module_c(help_texts):
    st.header("📊 Módulo C — Valoración de Bonos")
    
    # Información introductoria
    with st.expander("ℹ️ ¿Qué es la valoración de bonos?", expanded=False):
        st.markdown("""
        La valoración de bonos calcula el *valor presente* de todos los flujos futuros que 
        generará el bono (cupones y principal). Este valor depende de:
        - *Tasa cupón*: Interés que paga el bono periódicamente
        - *Tasa de retorno*: Rendimiento que exige el mercado/inversionista
        - *Relación*: Si la tasa de retorno > tasa cupón → bono con descuento (vale menos)
        """)
    
    # Configuración de entrada
    st.subheader("⚙️ Parámetros del Bono")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        face_value = st.number_input(
            "💵 Valor Nominal (USD)",
            min_value=0.0, value=1000.0, step=100.0,
            help=help_texts.get("valor_nominal", "Valor del bono al vencimiento")
        )
        
        coupon_rate = st.number_input(
            "🎫 Tasa Cupón (% anual)",
            min_value=0.0, max_value=100.0, value=5.0, step=0.1,
            help=help_texts.get("tasa_coupon", "Tasa de interés que paga el bono")
        )
    
    with col2:
        payment_freq = st.selectbox(
            "📅 Frecuencia de Pago",
            ["Mensual", "Bimestral", "Trimestral", "Cuatrimestral", "Semestral", "Anual"],
            index=4,  # Semestral por defecto
            help=help_texts.get("frecuencia_pago_bono", "Cada cuánto paga cupones")
        )
        
        years_to_maturity = st.number_input(
            "⏱️ Plazo (años)",
            min_value=0.1, max_value=50.0, value=10.0, step=0.5,
            help=help_texts.get("plazo_bono", "Años hasta el vencimiento")
        )
    
    with col3:
        required_yield = st.number_input(
            "📈 Tasa de Retorno Requerida (% anual)",
            min_value=0.0, max_value=50.0, value=6.0, step=0.1,
            help=help_texts.get("tasa_retorno_bono", "Rendimiento exigido por el inversionista")
        )
        
        # Opción para cambiar entre TEA y Tasa Nominal
        use_tea = st.checkbox(
            "Usar TEA (Tasa Efectiva Anual)",
            value=True,
            help="Si está desmarcado, se usará tasa nominal simple"
        )
    
    # Botón de cálculo
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        calculate = st.button("🧮 Calcular Valor del Bono", use_container_width=True, type="primary")
    
    if calculate:
        errors = validate_module_c(
            face_value=face_value,
            coupon_rate=coupon_rate,
            required_yield=required_yield,
            years_to_maturity=years_to_maturity
        )
        
        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            try:
                # Calcular valor del bono
                df_flows, pv_total, summary = bond_present_value(
                    face_value=face_value,
                    coupon_rate=coupon_rate,
                    payment_freq=payment_freq,
                    years_to_maturity=years_to_maturity,
                    required_yield=required_yield,
                    use_tea=use_tea
                )
                
                # ═══════════════════════════════════════════════════════
                # SECCIÓN 1: RESULTADO PRINCIPAL
                # ═══════════════════════════════════════════════════════
                st.markdown("---")
                st.subheader("💰 Resultado de la Valoración")
                
                col_m1, col_m2, col_m3 = st.columns(3)
                
                with col_m1:
                    st.metric(
                        "Valor Presente del Bono",
                        f"${pv_total:,.2f}",
                        delta=f"${summary['premium_discount']:,.2f} ({summary['premium_discount_pct']:+.2f}%)",
                        delta_color="normal"
                    )
                
                with col_m2:
                    st.metric(
                        "VP de Cupones",
                        f"${summary['vp_coupons']:,.2f}"
                    )
                
                with col_m3:
                    st.metric(
                        "VP del Principal",
                        f"${summary['vp_principal']:,.2f}"
                    )
                
                # ═══════════════════════════════════════════════════════
                # SECCIÓN 2: INTERPRETACIÓN
                # ═══════════════════════════════════════════════════════
                st.markdown("---")
                st.subheader("📖 Interpretación del Resultado")
                
                # Determinar tipo de bono
                if pv_total > face_value:
                    bond_type = "*Prima (Premium)*"
                    bond_icon = "📈"
                    interpretation = f"""
                    El bono cotiza *sobre la par* (con prima). Esto significa que:
                    - El valor presente (${pv_total:,.2f}) es *mayor* que el valor nominal (${face_value:,.2f})
                    - La tasa cupón ({coupon_rate}%) es *mayor* que la tasa de retorno requerida ({required_yield}%)
                    - Los inversionistas están dispuestos a pagar más porque el bono ofrece cupones atractivos
                    - *Ganancia adicional*: ${summary['premium_discount']:,.2f} ({summary['premium_discount_pct']:.2f}%)
                    """
                elif pv_total < face_value:
                    bond_type = "*Descuento (Discount)*"
                    bond_icon = "📉"
                    interpretation = f"""
                    El bono cotiza *bajo la par* (con descuento). Esto significa que:
                    - El valor presente (${pv_total:,.2f}) es *menor* que el valor nominal (${face_value:,.2f})
                    - La tasa cupón ({coupon_rate}%) es *menor* que la tasa de retorno requerida ({required_yield}%)
                    - Los inversionistas pagan menos porque el bono ofrece cupones menos atractivos que el mercado
                    - *Descuento*: ${summary['premium_discount']:,.2f} ({summary['premium_discount_pct']:.2f}%)
                    """
                else:
                    bond_type = "*A la Par*"
                    bond_icon = "➡️"
                    interpretation = f"""
                    El bono cotiza *a la par*. Esto significa que:
                    - El valor presente (${pv_total:,.2f}) es *igual* al valor nominal (${face_value:,.2f})
                    - La tasa cupón ({coupon_rate}%) es *igual* a la tasa de retorno requerida ({required_yield}%)
                    - El bono está valorado exactamente a su valor nominal
                    """
                
                st.info(f"{bond_icon} *Tipo de Bono*: {bond_type}")
                st.markdown(interpretation)
                
                with st.expander("🔍 Detalles del Cálculo", expanded=False):
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.write(f"*Periodos totales:* {summary['total_periods']}")
                        st.write(f"*Pago de cupón periódico:* ${summary['coupon_payment']:,.2f}")
                        st.write(f"*Total cupones a recibir:* ${summary['total_coupons']:,.2f}")
                    with col_d2:
                        st.write(f"*Tasa descuento periódica:* {summary['discount_rate_periodic']:.4f}%")
                        st.write(f"*Tipo de tasa:* {'TEA' if use_tea else 'Nominal'}")
                
                # ═══════════════════════════════════════════════════════
                # SECCIÓN 3: TABLA DETALLADA DE FLUJOS
                # ═══════════════════════════════════════════════════════
                st.markdown("---")
                st.subheader("📋 Tabla de Flujos Descontados (Detalle por Periodo)")
                
                df_display = df_flows.copy()
        
                st.dataframe(
                    df_display.style.format({
                        'Cupón': '${:,.2f}',
                        'Principal': '${:,.2f}',
                        'Flujo Total': '${:,.2f}',
                        'Factor Descuento': '{:.6f}',
                        'Valor Presente': '${:,.2f}'
                    }).background_gradient(
                        subset=['Valor Presente'],
                        cmap='Blues',
                        vmin=df_display['Valor Presente'].min(),
                        vmax=df_display['Valor Presente'].max()
                    ).set_properties(**{
                        'text-align': 'right'
                    }).set_table_styles([
                        {'selector': 'th', 'props': [('text-align', 'center'), ('font-weight', 'bold')]}
                    ]),
                    use_container_width=True,
                    height=400
                )
           
                csv = df_display.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar tabla como CSV",
                    data=csv,
                    file_name=f"bono_flujos_{payment_freq.lower()}.csv",
                    mime="text/csv"
                )
                
                # ═══════════════════════════════════════════════════════
                # SECCIÓN 4: GRÁFICO DE BARRAS APILADAS
                # ═══════════════════════════════════════════════════════
                st.markdown("---")
                st.subheader("📊 Visualización de Valores Presentes por Periodo")
                
     
                df_flows['VP Cupón'] = df_flows['Cupón'] * df_flows['Factor Descuento']
                df_flows['VP Principal'] = df_flows['Principal'] * df_flows['Factor Descuento']
                
           
                fig = go.Figure()
                
          
                fig.add_trace(go.Bar(
                    x=df_flows['Periodo'],
                    y=df_flows['VP Cupón'].round(2),
                    name='VP Cupones',
                    marker_color='#4A90E2',
                    text=df_flows['VP Cupón'].apply(lambda x: f'${x:,.0f}' if x > 0 else ''),
                    textposition='inside',
                    hovertemplate='<b>Periodo %{x}</b><br>' +
                                  'VP Cupón: $%{y:,.2f}<br>' +
                                  '<extra></extra>'
                ))
                
            
                fig.add_trace(go.Bar(
                    x=df_flows['Periodo'],
                    y=df_flows['VP Principal'].round(2),
                    name='VP Principal',
                    marker_color='#7B68EE',
                    text=df_flows['VP Principal'].apply(lambda x: f'${x:,.0f}' if x > 0 else ''),
                    textposition='inside',
                    hovertemplate='<b>Periodo %{x}</b><br>' +
                                  'VP Principal: $%{y:,.2f}<br>' +
                                  '<extra></extra>'
                ))
                
  
                fig.update_layout(
                    barmode='stack',
                    title={
                        'text': 'Valor Presente Descontado por Periodo (Cupones + Principal)',
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    xaxis_title='Periodo',
                    yaxis_title='Valor Presente (USD)',
                    hovermode='x unified',
                    template='plotly_white',
                    height=500,
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
         
                st.info("""
                💡 *Interpretación del gráfico:*
                - Las barras azules representan el valor presente de los cupones periódicos
                - La barra morada (periodo final) representa el valor presente del principal
                - La altura total de cada barra es el VP total de ese periodo
                - Note cómo los VP disminuyen con el tiempo debido al descuento temporal
                """)
                
                # Gráfico Solo cupones para comparación más clara
                st.markdown("---")
                st.subheader("📉 Evolución del Valor Presente de Cupones")
                
                fig2 = go.Figure()
                
                # Línea de VP de cupones
                fig2.add_trace(go.Scatter(
                    x=df_flows['Periodo'],
                    y=df_flows['VP Cupón'].round(2),
                    mode='lines+markers',
                    name='VP Cupón',
                    line=dict(color='#4A90E2', width=3),
                    marker=dict(size=8, color='#4A90E2'),
                    fill='tozeroy',
                    fillcolor='rgba(74, 144, 226, 0.2)',
                    hovertemplate='<b>Periodo %{x}</b><br>' +
                                  'VP Cupón: $%{y:,.2f}<br>' +
                                  '<extra></extra>'
                ))
                
                fig2.update_layout(
                    title={
                        'text': 'Disminución del Valor Presente de Cupones por Efecto del Descuento',
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    xaxis_title='Periodo',
                    yaxis_title='Valor Presente del Cupón (USD)',
                    hovermode='x unified',
                    template='plotly_white',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                st.caption("Este gráfico muestra cómo el mismo cupón vale menos en términos presentes cuanto más alejado esté en el tiempo.")
                
                # Gráfico Composición del VP
                st.markdown("---")
                st.subheader("🥧 Composición del Valor Presente")
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=['Cupones', 'Principal'],
                    values=[summary['vp_coupons'], summary['vp_principal']],
                    hole=0.4,
                    marker_colors=['#4A90E2', '#7B68EE'],
                    textinfo='label+percent+value',
                    texttemplate='<b>%{label}</b><br>$%{value:,.0f}<br>(%{percent})',
                    hovertemplate='<b>%{label}</b><br>' +
                                  'Valor: $%{value:,.2f}<br>' +
                                  'Porcentaje: %{percent}<br>' +
                                  '<extra></extra>'
                )])
                
                fig_pie.update_layout(
                    title={
                        'text': f'Distribución del VP Total: ${pv_total:,.2f}',
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
                
        
                st.session_state['module_c_result'] = {
                    'df_flows': df_flows,
                    'pv_total': pv_total,
                    'summary': summary,
                    'face_value': face_value,
                    'coupon_rate': coupon_rate,
                    'years': years_to_maturity,
                    'yield': required_yield,
                    'payment_freq': payment_freq,
                    'use_tea': use_tea
                }
                
                st.success("✅ Cálculo completado exitosamente")
                
            except Exception as e:
                st.error(f"❌ Error en el cálculo: {str(e)}")
                st.exception(e)