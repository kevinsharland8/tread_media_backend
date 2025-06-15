from fastapi import HTTPException, APIRouter, Depends, status
from models import Distance, Distance_id
from db import (
    get_postgres,
    fetch_with_error_handling,
    patch_with_error_handling,
    delete_with_error_handling,
    insert_with_error_handling,
)
from typing import List
import asyncpg

distance_router = APIRouter(prefix="/distance", tags=["distance"])


@distance_router.get(
    "/", response_model=List[Distance_id], status_code=status.HTTP_200_OK
)
async def get_distance(
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Distance_id]:
    query = "select id, distance from distance;"
    return await fetch_with_error_handling(db_pool=db_pool, query=query, model=Distance_id)


@distance_router.get(
    "/{distance_id}", response_model=Distance_id, status_code=status.HTTP_200_OK
)
async def single_distance(
    distance_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[Distance_id]:
    if not distance_id:
        raise HTTPException(status_code=400, detail="No id provided")
    query = """
    select id, distance from distance where id = $1;
    """
    return await fetch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=distance_id, model=Distance_id
    )


@distance_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_distance(
    distance: Distance,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not distance:
        raise HTTPException(status_code=400, detail="No fields provided for insert")
    query = """
    INSERT INTO distance (distance)
    VALUES ($1)
    RETURNING id, distance;
    """
    query_filters = [
        distance.distance,
    ]
    return await insert_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Distance
    )


@distance_router.patch("/{distance_id}", status_code=status.HTTP_200_OK)
async def update_distance(
    distance_id: int,
    distance: Distance,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not distance:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    query = f"""UPDATE distance SET 
    distance = $1 WHERE id = $2;"""
    query_filters = [
        distance.distance,
        distance_id,
    ]
    return await patch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=Distance
    )


@distance_router.delete("/{distance_id}", status_code=status.HTTP_200_OK)
async def delete_distance(
    distance_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not distance_id:
        raise HTTPException(status_code=400, detail="No id provided for deleting")
    query = f"""
    delete from distance where id = $1;
    """
    return await delete_with_error_handling(db_pool=db_pool, query=query, query_filters=distance_id, model=Distance)
