from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

custom_page_width = 3 * landscape(letter)[0]
custom_page_height = landscape(letter)[1]
custom_page_size = (custom_page_width, custom_page_height)


def generate_pdf_from_data(data):
    pdf_path = "static/inventory.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(custom_page_size))
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    desc_style = styles["BodyText"]
    title_style.alignment = 1  # Center align
    desc_style.alignment = 1  # Center align

    for section in data:
        title = section.get("title")
        description = section.get("description")
        table_data = section.get("data")

        if title:
            title_para = Paragraph(title, title_style)
            elements.append(title_para)
            elements.append(Spacer(1, 12))

        if description:
            desc_para = Paragraph(description, desc_style)
            elements.append(desc_para)
            elements.append(Spacer(1, 12))

        if table_data:
            table = Table(table_data, repeatRows=1)
            table_style = [
                ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ]
            table.setStyle(TableStyle(table_style))
            elements.append(table)
            elements.append(Spacer(1, 24))

    doc.build(elements)
    return pdf_path
