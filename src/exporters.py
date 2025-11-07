from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import matplotlib.pyplot as plt
import io
import os

def create_header_footer(canvas, doc):
    """Crea encabezado y pie de página para cada página del PDF"""
    canvas.saveState()
    
    # Encabezado
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(colors.HexColor('#1f4788'))
    canvas.drawString(inch, letter[1] - 0.5*inch, "Simulador de Finanzas Corporativas")
    
    # Línea separadora
    canvas.setStrokeColor(colors.HexColor('#1f4788'))
    canvas.setLineWidth(1.5)
    canvas.line(inch, letter[1] - 0.6*inch, letter[0] - inch, letter[1] - 0.6*inch)
    
    # Pie de página
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    canvas.drawString(inch, 0.5*inch, f"Generado: {fecha}")
    canvas.drawRightString(letter[0] - inch, 0.5*inch, f"Página {doc.page}")
    
    canvas.restoreState()

def create_matplotlib_chart(df, chart_type='line', title='', xlabel='', ylabel=''):
    """Crea gráficos de matplotlib y los convierte a imagen para el PDF"""
    fig, ax = plt.subplots(figsize=(6, 3.5))
    
    if chart_type == 'line':
        ax.plot(df.index, df.values, color='#1f4788', linewidth=2, marker='o', markersize=4)
    elif chart_type == 'bar':
        ax.bar(df.index, df.values, color='#4a90e2', alpha=0.8)
    
    ax.set_title(title, fontsize=12, fontweight='bold', color='#1f4788')
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    # Convertir a bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

def format_currency(value):
    """Formatea valores como moneda USD con 2 decimales"""
    try:
        return f"${float(value):,.2f}"
    except:
        return str(value)

def export_to_pdf(results, filename):
    """
    Exporta los resultados a un PDF profesional con gráficas, tablas y formato mejorado
    
    Args:
        results: Diccionario con los resultados de los módulos
        filename: Nombre del archivo PDF a generar
    """
    # Crear documento
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=1.2*inch,
        bottomMargin=0.8*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Portada
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("REPORTE FINANCIERO", title_style))
    elements.append(Paragraph("Simulador de Finanzas Corporativas", heading_style))
    elements.append(Spacer(1, 0.5*inch))
    
    meses_es = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
        'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
        'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
        'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    fecha_ingles = datetime.now().strftime("%d de %B de %Y")
    for eng, esp in meses_es.items():
        fecha_ingles = fecha_ingles.replace(eng, esp)
    fecha = fecha_ingles

    elements.append(Paragraph(f"<para alignment='center'>{fecha}</para>", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen ejecutivo
    elements.append(Paragraph("Resumen Ejecutivo", heading_style))
    summary_data = []
    
    if 'module_a_result' in results:
        final_balance = results['module_a_result'].get('final_balance', 0)
        summary_data.append(['Módulo A - Capital Acumulado', format_currency(final_balance)])
    
    if 'module_b_result' in results:
        res = results['module_b_result']
        if res.get('tipo') == 'cobro_total':
            summary_data.append(['Módulo B - Retiro Total Neto', format_currency(res.get('neto', 0))])
        else:
            summary_data.append(['Módulo B - Pensión Mensual Neta', format_currency(res.get('neto_mensual', 0))])
    
    if 'module_c_result' in results:
        pv = results['module_c_result'].get('pv_total', 0)
        summary_data.append(['Módulo C - Valor Presente del Bono', format_currency(pv)])
    
    if summary_data:
        summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f0fe')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f4788')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f4788'))
        ]))
        elements.append(summary_table)
    
    elements.append(PageBreak())
    
    # MÓDULO A - Crecimiento de Cartera
    if 'module_a_result' in results:
        elements.append(Paragraph("Módulo A: Crecimiento de Cartera", heading_style))
        
        res_a = results['module_a_result']
        df = res_a.get('df')
        final_balance = res_a.get('final_balance', 0)
        initial_amount = res_a.get('initial_amount', 0)
        years = res_a.get('years', 0)
        tea = res_a.get('tea', 0)
        
        # Parámetros de entrada
        elements.append(Paragraph("Parámetros de Simulación", subheading_style))
        
        params_data = [
            ['Monto Inicial', format_currency(initial_amount)],
            ['Plazo', f"{years} años"],
            ['Tasa Efectiva Anual (TEA)', f"{tea}%"],
            ['Capital Final Acumulado', format_currency(final_balance)]
        ]
        
        params_table = Table(params_data, colWidths=[3*inch, 2.5*inch])
        params_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (1, -1), (1, -1), colors.HexColor('#d4edda')),
            ('FONTNAME', (1, -1), (1, -1), 'Helvetica-Bold')
        ]))
        elements.append(params_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Gráfica de crecimiento
        if df is not None and len(df) > 0:
            elements.append(Paragraph("Evolución del Capital", subheading_style))
            
            try:
                import pandas as pd
                # Crear gráfico con ambas series
                fig, ax = plt.subplots(figsize=(8, 4))

                # Solo línea de Saldo Total
                ax.plot(df['Periodo'], df['Saldo_Final'], color='#1f4788', linewidth=2, marker='o', markersize=3)

                ax.set_title('Evolución del Capital', fontsize=12, fontweight='bold', color='#1f4788')
                ax.set_xlabel('Periodo')
                ax.set_ylabel('USD')
                ax.grid(True, alpha=0.3, linestyle='--')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                plt.tight_layout()
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                img = Image(img_buffer, width=5.5*inch, height=3*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                elements.append(Paragraph(f"<para color='red'>Error al generar gráfica: {str(e)}</para>", normal_style))
            
            # Tabla detallada (primeros y últimos 5 periodos)
            if len(df) > 8:
                elements.append(PageBreak())
            elements.append(Paragraph("Detalle de Periodos", subheading_style))
            
            if len(df) > 10:
                df_display = pd.concat([df.head(5), df.tail(5)])
                elements.append(Paragraph("<para><i>Mostrando primeros y últimos 5 periodos</i></para>", normal_style))
            else:
                df_display = df
            
            table_data = [['Periodo', 'Aporte', 'Saldo Inicial', 'Interés', 'Saldo Final']]
            
            for _, row in df_display.iterrows():
                table_data.append([
                    str(int(row['Periodo'])),
                    format_currency(row['Aporte']),
                    format_currency(row['Saldo_Inicial']),
                    format_currency(row['Interes']),
                    format_currency(row['Saldo_Final'])
                ])
            
            detail_table = Table(table_data, colWidths=[0.8*inch, 1.2*inch, 1.4*inch, 1.2*inch, 1.4*inch])
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
            ]))
            elements.append(detail_table)
        
        elements.append(PageBreak())
    
    # MÓDULO B - Proyección de Jubilación
    if 'module_b_result' in results:
        elements.append(Paragraph("Módulo B: Proyección de Jubilación", heading_style))
        
        res_b = results['module_b_result']
        tipo = res_b.get('tipo', '')
        
        if tipo == 'cobro_total':
            elements.append(Paragraph("Opción Seleccionada: Cobro Total", subheading_style))
            
            retirement_data = [
                ['Capital Bruto Acumulado', format_currency(res_b.get('bruto', 0))],
                ['Impuesto Aplicado', format_currency(res_b.get('impuesto', 0))],
                ['Monto Neto Disponible', format_currency(res_b.get('neto', 0))]
            ]
            
        else:  # pension_mensual
            elements.append(Paragraph("Opción Seleccionada: Pensión Mensual", subheading_style))
            
            retirement_data = [
                ['Capital Bruto Acumulado', format_currency(res_b.get('capital_bruto', 0))],
                ['Impuesto sobre Ganancias', format_currency(res_b.get('impuesto', 0))],
                ['Capital Neto Disponible', format_currency(res_b.get('capital_neto', 0))],
                ['', ''],
                ['Pensión Mensual (Bruto)', format_currency(res_b.get('bruto_mensual', 0))],
                ['Pensión Mensual (Neto)', format_currency(res_b.get('neto_mensual', 0))]
            ]
        
        retirement_table = Table(retirement_data, colWidths=[3.5*inch, 2*inch])
        retirement_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (1, -1), (1, -1), colors.HexColor('#d4edda')),
            ('FONTNAME', (1, -1), (1, -1), 'Helvetica-Bold')
        ]))
        elements.append(retirement_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Nota informativa
        note_text = """
        <para><b>Nota:</b> Los impuestos se calculan sobre las ganancias de capital 
        (diferencia entre capital final e inversión inicial). Las tasas aplicables son:
        29.5% para fuente extranjera o 5% para bolsa local peruana.</para>
        """
        elements.append(Paragraph(note_text, normal_style))
        
        elements.append(PageBreak())
    
    # MÓDULO C - Valoración de Bonos
    if 'module_c_result' in results:
        elements.append(Paragraph("Módulo C: Valoración de Bonos", heading_style))
        
        res_c = results['module_c_result']
        df_flows = res_c.get('df_flows')
        pv_total = res_c.get('pv_total', 0)
        face_value = res_c.get('face_value', 0)
        coupon_rate = res_c.get('coupon_rate', 0)
        years = res_c.get('years', 0)
        required_yield = res_c.get('yield', 0)
        
        # Parámetros del bono
        elements.append(Paragraph("Características del Bono", subheading_style))
        
        bond_params = [
            ['Valor Nominal', format_currency(face_value)],
            ['Tasa Cupón (TEA)', f"{coupon_rate}%"],
            ['Plazo', f"{years} años"],
            ['Tasa de Retorno Esperada', f"{required_yield}%"],
            ['Valor Presente del Bono', format_currency(pv_total)]
        ]
        
        bond_table = Table(bond_params, colWidths=[3.5*inch, 2*inch])
        bond_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (1, -1), (1, -1), colors.HexColor('#d4edda')),
            ('FONTNAME', (1, -1), (1, -1), 'Helvetica-Bold')
        ]))
        elements.append(bond_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Gráfica de flujos descontados
        if df_flows is not None and len(df_flows) > 0:
            elements.append(Paragraph("Valor Presente por Periodo", subheading_style))
            
            try:
                import pandas as pd
                # Crear gráfico mejorado
                fig, ax = plt.subplots(figsize=(8, 4))
                
                # Gráfico de barras para valores presentes
                bars = ax.bar(df_flows['Periodo'], df_flows['Valor Presente'], 
                            color='#4a90e2', alpha=0.8, edgecolor='#1f4788', linewidth=0.5)
                
                # Destacar el último periodo (valor nominal + cupón)
                if len(df_flows) > 0:
                    bars[-1].set_color('#FF4B4B')  # Última barra en rojo
                
                ax.set_title('Valor Presente de Flujos por Periodo', fontsize=12, fontweight='bold', color='#1f4788')
                ax.set_xlabel('Periodo')
                ax.set_ylabel('Valor Presente (USD)')
                ax.grid(True, alpha=0.3, linestyle='--', axis='y')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                # Rotar etiquetas del eje X si hay muchos periodos
                if len(df_flows) > 12:
                    plt.xticks(rotation=45)
                
                plt.tight_layout()
                
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                img = Image(img_buffer, width=5.5*inch, height=3*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
            except Exception as e:
                elements.append(Paragraph(f"<para color='red'>Error al generar gráfica: {str(e)}</para>", normal_style))
            
            # Tabla de flujos detallada
            if len(df_flows) > 8:
                elements.append(PageBreak())
            elements.append(Paragraph("Flujos de Caja Descontados", subheading_style))
            
            if len(df_flows) > 10:
                df_display = pd.concat([df_flows.head(5), df_flows.tail(5)])
                elements.append(Paragraph("<para><i>Mostrando primeros y últimos 5 periodos</i></para>", normal_style))
            else:
                df_display = df_flows
            
            table_data = [['Periodo', 'Cupón', 'Principal', 'Flujo Total', 'Valor Presente']]

            for _, row in df_display.iterrows():
                table_data.append([
                    str(int(row['Periodo'])),
                    format_currency(row['Cupón']),
                    format_currency(row['Principal']),
                    format_currency(row['Flujo Total']),
                    format_currency(row['Valor Presente'])
                ])
            
            flows_table = Table(table_data, colWidths=[0.8*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            flows_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
            ]))
            elements.append(flows_table)
    
    # Pie de página con disclaimer
    elements.append(Spacer(1, 0.5*inch))
    disclaimer = """
    <para alignment='center' fontSize='8' color='grey'>
    <i>Este reporte ha sido generado automáticamente por el Simulador de Finanzas Corporativas.
    Los cálculos son referenciales y deben ser validados por un asesor financiero profesional.</i>
    </para>
    """
    elements.append(Paragraph(disclaimer, normal_style))
    
    # Construir PDF
    doc.build(elements, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
