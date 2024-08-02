import openpyxl
from openpyxl_image_loader import SheetImageLoader
import requests
import os.path

import pandas as pd

from config import SPREADSHEET_ID, SHEET_NAME


def extract_images_from_excel(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb[SHEET_NAME]
    image_loader = SheetImageLoader(sheet)

    image_dir = 'static/images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    image_positions = {}

    for row in sheet.iter_rows():
        for cell in row:
            cell_address = cell.coordinate
            if image_loader.image_in(cell_address):
                image = image_loader.get(cell_address)
                image_path = os.path.join(image_dir, f'image_{cell_address}.png')
                image.save(image_path)
                image_positions[cell_address] = f'{image_dir}/image_{cell_address}.png'

    return image_positions


# Download the Google sheet data and process locally
def download_google_sheet(spreadsheet_id, sheet_name, out_file):
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx'
    response = requests.get(url)
    if response.status_code == 200:
        with open(out_file, 'wb') as f:
            f.write(response.content)
            print('Table file saved to: {}'.format(out_file))

        # load excel with image
        # extract images
        image_positions = extract_images_from_excel(out_file)
        # read the tabular data
        df = pd.read_excel(out_file, engine='openpyxl', sheet_name=sheet_name)
        # insert image paths into df
        for cell_address, img_path in image_positions.items():
            col, row = openpyxl.utils.cell.coordinate_from_string(cell_address)
            # print(col, row): M 2
            row_idx = row - 2
            df.at[row_idx, 'Photo'] = img_path
        print(df.head())
        return df

    else:
        print(f'Error downloading Google Sheet: {response.status_code}')
        return


if __name__ == "__main__":
    download_google_sheet(SPREADSHEET_ID, SHEET_NAME, "copy.xlsx")