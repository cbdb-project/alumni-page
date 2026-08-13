
SHEET_NAME = "alumni"
SPREADSHEET_ID = "19SUbSezEZ_ObEqfoNY3BDAM8z3cyBR-raql0Rs7_N3A"

# Columns to publish, in output order. Selecting by name rather than dropping
# unwanted ones keeps the output stable when editors add, remove or reorder
# columns in the spreadsheet.
# Email and gmail-calendar are deliberately withheld from the public alumni page.
KEEP_COLUMN = [
    "LAST, First Name EN",
    "Chinese Name",
    "Home Institution",
    "Specialty",
    "Task",
    "Arrive/Depart",
    "Affiliation",
    "Photo",
]
