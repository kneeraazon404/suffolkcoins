from django.shortcuts import render
from google.oauth2.credentials import Credentials


def index(request):
    return render(request, "index.html")


from django.http import HttpResponse
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def inventory(request):
    # Step 1: Authenticate using the Service Account
    SERVICE_ACCOUNT_FILE = "credentials.json"

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive",
        ],
    )

    service = build("drive", "v3", credentials=credentials)

    # Step 2: Specify the Google Sheet ID
    SHEET_ID = "1SJ7sj2YSF-wpH4MwPt_OClkYV4Dlcy0lV9lThSpQXwA"

    # Step 3: Export Google Sheet as PDF
    request = service.files().export_media(fileId=SHEET_ID, mimeType="application/pdf")
    response = request.execute()

    # Step 4: Return the PDF as an HTTP response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="inventory.pdf"'
    response.write(request.execute())
    return response
