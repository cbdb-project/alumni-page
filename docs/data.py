import json
import math
import logging

from utils import download_google_sheet
from config import DROP_COLUMN, SPREADSHEET_ID, SHEET_NAME


def prepare_data():
    processed_data = []
    df = download_google_sheet(SPREADSHEET_ID, SHEET_NAME, "copy.xlsx")
    columns_to_remove = DROP_COLUMN
    df = df.drop(columns=columns_to_remove, errors='ignore')
    # hardcode here to drop the last column with wrong input area
    # df = df.iloc[:, :9]
    data = df.to_dict(orient='records')

    for record in data:
        # skip the empty lines between in boston and not in boston
        if isinstance(record.get("LAST, First Name EN"), float) and math.isnan(record.get("LAST, First Name EN")):
            continue
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = ""
            # if key == "Cell":
            #     if math.isnan(value):
            #         record[key] = ""
            #     else:
            #         record[key] = int(value)
            elif key == "Arrive/Depart":
                if isinstance(value, float) and math.isnan(value):
                    record[key] = ""
                else:
                    record[key] = str(value)
        processed_data.append(record)
    with open('data.json', 'w') as f:
        json.dump(processed_data, f)


if __name__ == "__main__":
    # Configure logging
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # logging.info("Starting data.py script")
    prepare_data()
    # logging.info("Updated docs/data.json successfully")
