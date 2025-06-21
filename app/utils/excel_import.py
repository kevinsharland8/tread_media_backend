import openpyxl
from openpyxl_image_loader import SheetImageLoader
import os
from utils.upload_google import upload_to_bucket
from db import get_postgres, insert_with_error_handling
from models import Event


async def insert_data(event: Event, event_image: str) -> Event:

    if not event:
        raise ValueError("No fields provided for insert")

    db_pool = await get_postgres()

    query = """
    INSERT INTO events (name, description, start_date, end_date, city, province, event_website, organizer, active, map_link, event_type_id, multi_day)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    RETURNING id, name, description, start_date, end_date, city, province, event_website, organizer, map_link, event_type_id, multi_day;
    """
    query_filters = [
        event.name,
        event.description,
        event.start_date,
        event.end_date,
        event.city,
        event.province,
        event.event_website,
        event.organizer,
        event.active,
        event.map_link,
        event.event_type_id,
        event.multi_day,
    ]
    unique_event_id = await insert_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event
    )

    query = """
    INSERT INTO event_images (event_id, headline, url) values ($1, $2, $3)
    RETURNING id, event_id, headline, url;
    """

    query_filters = [unique_event_id["result"], True, event_image]

    unique_event_image_id = await insert_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event
    )
    return {'results': [unique_event_id, unique_event_image_id]}

async def extract_from_file(file):
    workbook = openpyxl.load_workbook(file)
    # workbook = openpyxl.load_workbook("/home/kevin/projects/tread-events-python/app/utils/excel_with_image.xlsx")
    # workbook = openpyxl.load_workbook("/tmp/tmp5x7rdpxo.xlsx")
    sheet = workbook["Sheet1"]
    output_directory = "/home/kevin/projects/tread-events-python/images/"
    # Initialize image loader
    image_loader = SheetImageLoader(sheet)
    progress = True

    try:
        # get the header column
        headers = [cell.value for cell in sheet[1]]
        # min_row = the starting row, max_row = last row with data, min_col = starting column, max_col = last column with data
        for row in sheet.iter_rows(
            min_row=2, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column
        ):
            row_num = row[0].row  # Get the row number
            row_values = [cell.value for cell in row]
            row_dict = dict(zip(headers, row_values))
            event = Event(**row_dict)
            # need to update this if the image column changes
            image_cell = f"N{row_num}"
            if image_loader.image_in(image_cell):
                image = image_loader.get(image_cell)
                image_filename = f"image_row_{row_num}.png"
                complete_path_image = os.path.join(output_directory, image_filename)
                image.save(complete_path_image)
                try:
                    insert_into_tables = await insert_data(event, image_filename)
                except Exception as e:
                    print(f"there is a n error inserting the data {e}")
                try:
                    clean_name = f'eid_{insert_into_tables["results"][0]["result"]}_eiid_{insert_into_tables["results"][1]["result"]}.png'
                    # print(clean_name)
                    upload_to_bucket(complete_path_image, clean_name)
                except Exception as e:
                    print(f"there is a n error copying it to the bucket {e}")       
            else:
                progress = False
        return progress

    except Exception as e:
        print(f"error Processing file, {e}")
