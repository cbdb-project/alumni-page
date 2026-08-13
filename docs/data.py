import json
import math
import logging

from utils import download_google_sheet
from config import SPREADSHEET_ID, SHEET_NAME, KEEP_COLUMN


def prepare_data():
    processed_data = []
    df = download_google_sheet(SPREADSHEET_ID, SHEET_NAME, "docs/copy.xlsx")

    missing = [c for c in KEEP_COLUMN if c not in df.columns]
    if missing:
        logging.warning("Columns missing from the spreadsheet: %s", missing)
    df = df[[c for c in KEEP_COLUMN if c in df.columns]]

    data = df.to_dict(orient='records')

    for record in data:
        # skip the empty lines between in boston and not in boston
        if isinstance(record.get("LAST, First Name EN"), float) and math.isnan(record.get("LAST, First Name EN")):
            continue
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = ""
            elif key == "Arrive/Depart":
                if isinstance(value, float) and math.isnan(value):
                    record[key] = ""
                else:
                    record[key] = str(value)
        processed_data.append(record)
    with open('docs/data.json', 'w') as f:
        json.dump(processed_data, f)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting data.py script")
    prepare_data()
    logging.info("Updated docs/data.json successfully")
