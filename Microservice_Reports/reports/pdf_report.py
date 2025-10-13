# Archivo: generate_pdf.py

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import datetime
import json
import re

def generate_pdf(data, report_type=None, filename=None):
    """
    Genera un PDF dinámico en formato tabla a partir de cualquier JSON recibido.
    - data: lista o diccionario con datos a incluir.
    - report_type: opcional; si no se pasa, se infiere del contenido.
    - filename: opcional; si no se pasa, se genera automáticamente.
    """

    # --- Normalizar data ---
    if isinstance(data, dict):
        data = [data]
    if not data:
        data = [{"info": "No hay datos disponibles"}]

    # --- Inferir tipo de reporte dinámico ---
    if not report_type:
        first_key = list(data[0].keys())[0] if isinstance(data[0], dict) else "general"
        report_type = first_key.replace("_", " ").capitalize()

    # --- Nombre del archivo ---
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_type = re.sub(r'[^a-zA-Z0-9_]', '_', report_type)
    filename = filename or f"reporte_{safe_type}_{timestamp}.pdf"

    # --- Configuración base ---
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4), leftMargin=30, rightMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle('normal', parent=styles['Normal'], fontSize=8, leading=10)

    # --- Título ---
    title = Paragraph(f"<b>Reporte de {report_type.capitalize()}</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # --- Cabeceras dinámicas ---
    all_columns = set()
    for row in data:
        all_columns.update(row.keys())
    headers = list(all_columns)
    table_data = [[Paragraph(f"<b>{h}</b>", normal_style) for h in headers]]

    # --- Filas ---
    for row in data:
        row_values = []
        for h in headers:
            value = row.get(h, "")
            if isinstance(value, (dict, list)):
                formatted = json.dumps(value, indent=2, ensure_ascii=False)
            else:
                formatted = str(value)
            row_values.append(Paragraph(formatted, normal_style))
        table_data.append(row_values)

    # --- Calcular ancho de columnas dinámico ---
    page_width = landscape(A4)[0] - 80
    col_width = max(80, page_width / len(headers))
    col_widths = [col_width for _ in headers]

    # --- Tabla con estilo ---
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("WORDWRAP", (0, 0), (-1, -1), True),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # --- Footer ---
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generado automáticamente el {fecha}", styles["Normal"]))

    doc.build(elements)
    return filename