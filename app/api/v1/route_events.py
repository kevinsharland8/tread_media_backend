from fastapi import HTTPException, APIRouter, Depends, status
from models import Event, Event_id, EventMainDisplay
from db import (
    get_postgres,
    fetch_with_error_handling,
    patch_with_error_handling,
    delete_with_error_handling,
    insert_with_error_handling,
)
from typing import List
import asyncpg

event_router = APIRouter(prefix="/event", tags=["event"])


@event_router.get("/", response_model=List[Event_id], status_code=status.HTTP_200_OK)
async def event(
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Event_id]:
    query = "Select id, name, description, start_date, end_date, city, province, event_website, organizer, active, map_link, event_type_id, multi_day from events;"
    return await fetch_with_error_handling(db_pool=db_pool, query=query, model=Event_id)


@event_router.get(
    "/{event_id}", response_model=Event_id, status_code=status.HTTP_200_OK
)
async def single_event(
    event_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Event_id]:
    if not event_id:
        raise HTTPException(status_code=400, detail="No id provided")
    query = """
    select id, name, description, start_date, end_date, city, province, event_website, organizer, active, map_link, event_type_id, multi_day from events where id = $1;
    """
    return await fetch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=event_id, model=Event_id
    )


@event_router.get(
    "/details/{event_id}",
    response_model=EventMainDisplay,
    status_code=status.HTTP_200_OK,
)
async def details_event(
    event_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[EventMainDisplay]:
    if not event_id:
        raise HTTPException(status_code=400, detail="No id provided")
    query = """
    SELECT 
    e.id, e.name, e.description, e.start_date, e.end_date, e.city, e.province, e.event_website, e.organizer, e.active, e.map_link, e.multi_day,
    -- Aggregate event images
    json_agg(DISTINCT jsonb_build_object(
        'headline', ei.headline, 
        'url', ei.url
    )) AS images,
    -- Aggregate distances
    json_agg(DISTINCT jsonb_build_object(
        'day', ed.day, 
        'distance', ed.distance
    )) AS day_distance,
    et.type
    FROM events e
    JOIN event_images ei ON e.id = ei.event_id
    JOIN event_distances ed ON e.id = ed.event_id
    JOIN event_types et ON e.event_type_id = et.id
    WHERE e.id = $1 GROUP BY e.id, et.type;
    """
    data_returned =  await fetch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=event_id, model=EventMainDisplay
    )
    return data_returned


@event_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(
    event: Event,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event:
        raise HTTPException(status_code=400, detail="No fields provided for insert")
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
        event.multi_day
    ]
    return await insert_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event
    )


@event_router.patch("/{event_id}", status_code=status.HTTP_200_OK)
async def update_event(
    event_id: int,
    event: Event,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    query = f"""UPDATE events SET 
    name = $1, description = $2, start_date = $3, end_date = $4, city = $5, 
    province = $6, event_website = $7, organizer = $8, active = $9, map_link = $10, 
    event_type_id = $11, multi_day=$12 WHERE id = $13;"""
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
        event_id,
    ]
    return await patch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event
    )


@event_router.delete("/{event_id}", status_code=status.HTTP_200_OK)
async def delete_event(
    event_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event_id:
        raise HTTPException(status_code=400, detail="No id provided for deleting")
    query = f"""
    delete from events where id = $1;
    """
    return await delete_with_error_handling(
        db_pool=db_pool, query=query, query_filters=event_id, model=Event
    )
