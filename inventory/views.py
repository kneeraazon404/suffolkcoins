from django.shortcuts import render
import gspread


def index(request):
    return render(request, "index.html")


from django.shortcuts import render
import gspread
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Inventory
from django.core.files import File

custom_page_width = 4 * landscape(letter)[0]  # Quadruple the width
custom_page_height = 1 * landscape(letter)[1]  # Double the height

custom_page_size = (custom_page_width, custom_page_height)


def inventory(request):
    # get the inventory object
    sgs = gspread.service_account("credentials.json")
    sheet = sgs.open("inventory")

    # Assuming you want the first worksheet
    worksheet = sheet.get_worksheet(0)

    # Fetch all data from the worksheet
    raw_data = worksheet.get_all_values()
    header = raw_data[0]
    data_rows = raw_data[1:]

    # Convert parsed data to a format suitable for ReportLab
    table_data = [header] + data_rows

    # Create a new PDF with the name 'inventory.pdf'
    pdf_path = "static/inventory.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(custom_page_size))

    # Create the table with the data
    table = Table(table_data, repeatRows=1)

    # Add a grid and other styling
    table_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 14),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]
    table.setStyle(TableStyle(table_style))
    doc.build([table])

    # Check if the Inventory object exists
    inventory = Inventory.objects.first()
    if not inventory:
        inventory = Inventory()

    # Use Django's FileField handling to save the file
    with open(pdf_path, "rb") as pdf_file:
        inventory.file.save("inventory.pdf", File(pdf_file))
        inventory.save()

    context = {"pdf_path": inventory.file.url}
    return render(request, "inventory.html", context)
