from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_to_pdf(results, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    for title, data in results.items():
        elements.append(Paragraph(title, styles['Heading2']))
        elements.append(Spacer(1, 12))
        if isinstance(data, dict):
            table_data = [[k, str(v)] for k, v in data.items()]
        elif hasattr(data, 'to_dict'):
            d = data.to_dict('records')
            if d:
                table_data = [list(d[0].keys())]
                table_data += [list(row.values()) for row in d]
            else:
                table_data = [['Sin datos']]
        else:
            table_data = [['Resultado', str(data)]]
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 24))
    
    doc.build(elements)