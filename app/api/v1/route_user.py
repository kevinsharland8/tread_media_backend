from fastapi import HTTPException, APIRouter, Depends, status
from models import User, User_id
from db import (
    get_postgres,
    fetch_with_error_handling,
    patch_with_error_handling,
    delete_with_error_handling,
    insert_with_error_handling,
)
from typing import List
import asyncpg

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get(
    "/", response_model=List[User_id], status_code=status.HTTP_200_OK
)
async def get_users(
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[User_id]:
    query = "select id, email, first_name, last_name, google_id, created_at, updated_at from users;"
    return await fetch_with_error_handling(db_pool=db_pool, query=query, model=User_id)


@user_router.get(
    "/{user_id}", response_model=User_id, status_code=status.HTTP_200_OK
)
async def single_user(
    user_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[User_id]:
    if not user_id:
        raise HTTPException(status_code=400, detail="No id provided")
    query = """
    select id, email, first_name, last_name, google_id, created_at, updated_at from users where id = $1;
    """
    return await fetch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=user_id, model=User_id
    )


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: User,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not user:
        raise HTTPException(status_code=400, detail="No fields provided for insert")
    query = """
    INSERT INTO users (email, first_name, last_name, google_id, created_at, updated_at)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING id, email, first_name, last_name, google_id, created_at, updated_at;
    """
    query_filters = [
        user.email,
        user.first_name,
        user.last_name,
        user.google_id,
        user.created_at,
        user.updated_at,
    ]
    return await insert_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=User
    )


@user_router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user: User,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not user:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    query = f"""UPDATE users SET 
    email = $1, first_name = $2, last_name = $3, google_id = $4, created_at = $5, 
    updated_at = $6 WHERE id = $7;"""
    query_filters = [
        user.email,
        user.first_name,
        user.last_name,
        user.google_id,
        user.created_at,
        user.updated_at,
        user_id,
    ]
    return await patch_with_error_handling(
        db_pool=db_pool, query=query, query_filters=query_filters, model=User
    )


@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not user_id:
        raise HTTPException(status_code=400, detail="No id provided for deleting")
    query = f"""
    delete from users where id = $1;
    """
    return await delete_with_error_handling(db_pool=db_pool, query=query, query_filters=user_id, model=User)
