from fastapi import HTTPException, APIRouter, Depends, status
from models import Event_id, EventMainDisplay
from db import (
    get_postgres,
    fetch_with_error_handling,
)
from typing import List
import asyncpg

event_router = APIRouter(prefix="/event", tags=["event"])


@event_router.get("/", response_model=List[Event_id], status_code=status.HTTP_200_OK)
async def event(
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Event_id]:
    query = "Select id, name, description, start_date, end_date, city, province_id, event_website, organizer, active, map_link, multi_day from events;"
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
    select id, name, description, start_date, end_date, city, province_id, event_website, organizer, active, map_link, multi_day from events where id = $1;
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
select e.id, e.name, e.description, e.start_date, e.end_date, e.city, e.event_website, e.organizer, e.active, e.map_link, e.multi_day, p.p_name,
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
-- Aggregate distances
json_agg(DISTINCT jsonb_build_object(
'event_type', et.type
)) AS event_type
from 
events e
join event_event_types_junction eetj on e.id = eetj.event_id
join event_types et on et.id = eetj.event_type_id
join provinces p on e.province_id = p.id
join event_images ei on e.id = ei.event_id
join event_distances ed on e.id = ed.event_id
where e.id = $1
GROUP BY e.id, p.p_name
    """
    data_returned = await fetch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=event_id, model=EventMainDisplay
    )
    return data_returned
