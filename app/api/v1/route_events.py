from fastapi import HTTPException, APIRouter, Depends, status
from models import Event, Event_id
from db import (
    get_postgres,
    fetch_with_error_handling,
    patch_with_error_handling,
    delete_with_error_handling,
    insert_with_error_handling,
)
from typing import List
import asyncpg

event_router = APIRouter()


@event_router.get(
    "/all_events", response_model=List[Event_id], status_code=status.HTTP_200_OK
)
async def event(
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Event_id]:
    query = "Select id, event_name, event_description, start_date, end_date, province, event_date, event_website, organizer, active, headline_image, promotion_images, map_link from events;"
    return await fetch_with_error_handling(db_pool=db_pool, query=query, model=Event_id)


@event_router.get(
    "/event/{event_id}", response_model=List[Event_id], status_code=status.HTTP_200_OK
)
async def single_event(
    event_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Event_id]:
    if not event_id:
        raise HTTPException(status_code=400, detail="No id provided") 
    query = """
    select id, event_name, event_description, start_date, end_date, province, event_date, event_website, organizer, active, headline_image, promotion_images, map_link from events where id = $1;
    """
    return await fetch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=event_id, model=Event_id
    )


@event_router.post("/event", status_code=status.HTTP_201_CREATED)
async def create_event(
    event: Event,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event:
        raise HTTPException(status_code=400, detail="No fields provided for insert")    
    query = """
    INSERT INTO events (event_name, event_description, start_date, end_date, province, event_date, event_website, organizer, active, headline_image, promotion_images, map_link)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    RETURNING id, event_name, event_description, start_date, end_date, province, event_date, event_website, organizer, active, headline_image, promotion_images, map_link;
    """
    query_filters = [
        event.event_name,
        event.event_description,
        event.start_date,
        event.end_date,
        event.province,
        event.event_date,
        event.event_website,
        event.organizer,
        event.active,
        event.headline_image,
        event.promotion_images,
        event.map_link,
    ]
    return await insert_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event
    )


@event_router.patch("/event/{event_id}", status_code=status.HTTP_200_OK)
async def update_event(
    event_id: int,
    event: Event,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    query = f"""UPDATE events SET 
    event_name = $1, event_description = $2, start_date = $3, end_date = $4, province = $5, 
    event_date = $6, event_website = $7, organizer = $8, active = $9, headline_image = $10, 
    promotion_images = $11, map_link = $12 WHERE id = {event_id};"""
    query_filters = [
        event.event_name,
        event.event_description,
        event.start_date,
        event.end_date,
        event.province,
        event.event_date,
        event.event_website,
        event.organizer,
        event.active,
        event.headline_image,
        event.promotion_images,
        event.map_link,
    ]
    return await patch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event
    )


@event_router.delete("/event/{event_id}", status_code=status.HTTP_200_OK)
async def delete_event(
    event_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event_id:
        raise HTTPException(status_code=400, detail="No id provided for deleting")    
    query = f"""
    delete from events where id = {event_id};
    """
    return await delete_with_error_handling(db_pool=db_pool, query=query, model=Event)
