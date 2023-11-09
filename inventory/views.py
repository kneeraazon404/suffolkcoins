from django.shortcuts import render
from google.oauth2.credentials import Credentials

from django.http import HttpResponse
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from django.http import HttpResponse
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


def index(request):
    return render(request, "index.html")


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
    response_content = request.execute()

    # Step 4: Return the PDF as an HTTP response
    response = HttpResponse(response_content, content_type="application/pdf")
    # Use 'inline' to open in the browser
    response["Content-Disposition"] = 'inline; filename="inventory.pdf"'
    return response
