import openpyxl
from openpyxl_image_loader import SheetImageLoader
import os


def extract_from_file(file):
    workbook = openpyxl.load_workbook(file)
    # workbook = openpyxl.load_workbook("/home/kevin/projects/tread-events-python/app/utils/excel_with_image.xlsx")
    # workbook = openpyxl.load_workbook("/tmp/tmp5x7rdpxo.xlsx")
    sheet = workbook["event_test_data"]
    output_directory = "/home/kevin/projects/tread-events-python/images/"
    # Initialize image loader
    image_loader = SheetImageLoader(sheet)

    try:
        # min_row = the starting row, max_row = last row with data, min_col = starting column, max_col = last column with data
        for row in sheet.iter_rows(
            min_row=2, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column
        ):
            row_num = row[0].row  # Get the row number
            row_values = [cell.value for cell in row]
            print(f"Row {row_num} data: {row_values}")

            # need to update this if the image column changes
            image_cell = f"N{row_num}"
            if image_loader.image_in(image_cell):
                image = image_loader.get(image_cell)
                image_filename = f"image_row_{row_num}.png"
                print(image_filename)
                complete_path_image = os.path.join(output_directory, image_filename)
                image.save(complete_path_image)
    except Exception as e:
        print(f"error Processing file, {e}")
