import gspread
from django.core.files import File
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from .models import Inventory


def index(request):
    return render(request, "index.html")


custom_page_width = landscape(letter)[0]
custom_page_height = landscape(letter)[1]
custom_page_size = (custom_page_width, custom_page_height)


def inventory(request):
    sgs = gspread.service_account("credentials.json")
    sheet = sgs.open("inventory")
    worksheet = sheet.get_worksheet(0)
    raw_data = worksheet.get_all_values()

    # Process the data
    tables = []
    current_table = []
    for row in raw_data:
        if any(row):
            if not any(current_table):
                if len(row) == 1:
                    tables.append(row[0])
                else:
                    current_table.append(row)
            else:
                current_table.append(row)
        else:
            if any(current_table):
                tables.append(current_table)
                current_table = []

    if any(current_table):
        tables.append(current_table)

    pdf_path = "static/inventory.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(custom_page_size))
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    description_style = styles["BodyText"]
    title_style.alignment = 1
    description_style.alignment = 1

    content = []
    for item in tables:
        if isinstance(item, str):
            if len(item.split()) > 5:
                para = Paragraph(item, description_style)
            else:
                para = Paragraph(item, title_style)
            content.append(para)
            content.append(Spacer(1, 0.2 * inch))
        else:
            colWidths = [len(max(column, key=len)) * 7 for column in zip(*item)]
            table = Table(item, colWidths=colWidths, repeatRows=1)
            table_style = [
                ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
            ]
            table.setStyle(TableStyle(table_style))
            content.append(table)
            content.append(Spacer(1, 0.5 * inch))

    doc.build(content)

    inventory = Inventory.objects.first()
    if not inventory:
        inventory = Inventory()

    with open(pdf_path, "rb") as pdf_file:
        inventory.file.save("inventory.pdf", File(pdf_file))
        inventory.save()

    context = {"pdf_path": inventory.file.url}
    return render(request, "inventory.html", context)
