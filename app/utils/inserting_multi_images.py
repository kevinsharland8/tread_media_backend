import openpyxl
from openpyxl_image_loader import SheetImageLoader
import os
from utils.upload_google import upload_to_bucket
from db import get_postgres, insert_with_error_handling, fetch_with_error_handling
from models import Event


async def insert_data(event_id: int, event_image: str) -> Event:
    if not event_id:
        print('boom')
        raise ValueError("No event_id provided")
    db_pool = await get_postgres()
    query = """
    select * from events where id = $1;
    """
    event_checker = await fetch_with_error_handling(db_pool=db_pool, query=query, query_filters=event_id, model=Event)

    query = """
    INSERT INTO event_images (event_id, headline, url) values ($1, $2, $3)
    RETURNING id, event_id, headline, url;
    """
    query_filters = [event_id, False, event_image]

    unique_event_image_id = await insert_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event
    )
    return {'results': [event_checker, unique_event_image_id]}