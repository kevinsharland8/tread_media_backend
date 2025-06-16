from fastapi import HTTPException, APIRouter, Depends, status
from models import Event_type, Event_type_id
from db import (
    get_postgres,
    fetch_with_error_handling,
    patch_with_error_handling,
    delete_with_error_handling,
    insert_with_error_handling,
)
from typing import List
import asyncpg

event_type_router = APIRouter(prefix="/event_type", tags=["event_type"])


@event_type_router.get("/", response_model=List[Event_type_id], status_code=status.HTTP_200_OK)
async def event_type(
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Event_type_id]:
    query = "Select id, event_name from event_type;"
    return await fetch_with_error_handling(db_pool=db_pool, query=query, model=Event_type_id)


@event_type_router.get(
    "/{event_type_id}", response_model=Event_type_id, status_code=status.HTTP_200_OK
)
async def single_event_type(
    event_type_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Event_type_id]:
    if not event_type_id:
        raise HTTPException(status_code=400, detail="No id provided")
    query = """
    select id, event_name from event_type where id = $1;
    """
    return await fetch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=event_type_id, model=Event_type_id
    )


@event_type_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event_type(
    event_type: Event_type,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event_type:
        raise HTTPException(status_code=400, detail="No fields provided for insert")
    query = """
    INSERT INTO event_type (event_name)
    VALUES ($1)
    RETURNING id, event_name;
    """
    query_filters = [
        event_type.event_name,
    ]
    return await insert_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event_type
    )


@event_type_router.patch("/{event_type_id}", status_code=status.HTTP_200_OK)
async def update_event_type(
    event_type_id: int,
    event_type: Event_type,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event_type:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    query = f"""UPDATE event_type SET 
    event_name = $1 WHERE id = $2;"""
    query_filters = [
        event_type.event_name,
        event_type_id,
    ]
    return await patch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Event_type
    )


@event_type_router.delete("/{event_type_id}", status_code=status.HTTP_200_OK)
async def delete_event(
    event_type_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not event_type_id:
        raise HTTPException(status_code=400, detail="No id provided for deleting")
    query = f"""
    delete from event_type where id = $1;
    """
    return await delete_with_error_handling(db_pool=db_pool, query=query, query_filters=event_type_id, model=Event_type)
