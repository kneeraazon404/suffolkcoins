import gspread

sgs = gspread.service_account()
sheet = sgs.open("inventory")

# Assuming you want the first worksheet
worksheet = sheet.get_worksheet(0)

# Fetch all data from the worksheet
data = worksheet.get_all_values()

# Print the data
for row in data:
    print(row)
