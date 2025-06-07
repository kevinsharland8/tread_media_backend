from fastapi import HTTPException, APIRouter, Depends, status
from models import User, User_id
from db import get_postgres
from typing import List
import asyncpg

user_router = APIRouter()


@user_router.get(
    "/all_users", response_model=List[User_id], status_code=status.HTTP_200_OK
)
async def get_users(
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[User_id]:
    query = """
    select id, email, first_name, last_name, google_id, created_at, updated_at from users;
    """
    try:
        async with db_pool.acquire() as conn:
            results = await conn.fetch(query)
            return [User_id(**dict(result)) for result in results]
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")


@user_router.get(
    "/user/{user_id}", response_model=List[User], status_code=status.HTTP_200_OK
)
async def single_user(
    user_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[User]:
    query = """
    select email, first_name, last_name, google_id, created_at, updated_at from users where id = $1;
    """
    try:
        async with db_pool.acquire() as conn:
            results = await conn.fetch(query, user_id)
            return [User(**dict(result)) for result in results]
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")


@user_router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: User,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    query = """
    INSERT INTO users (email, first_name, last_name, google_id, created_at, updated_at)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING id, email, first_name, last_name, google_id, created_at, updated_at;
    """
    try:
        async with db_pool.acquire() as conn:
            result = await conn.execute(
                query,
                user.email,
                user.first_name,
                user.last_name,
                user.google_id,
                user.created_at,
                user.updated_at,
            )
            return {"detail": "User created successfully"}
    except Exception as e:
        print(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")


@user_router.patch("/user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user: User,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    if not user:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    query = f"""UPDATE users SET 
    email = $1, first_name = $2, last_name = $3, google_id = $4, created_at = $5, 
    updated_at = $6 WHERE id = {user_id};"""
    try:
        async with db_pool.acquire() as conn:
            result = await conn.execute(
                query,
                user.email,
                user.first_name,
                user.last_name,
                user.google_id,
                user.created_at,
                user.updated_at,
            )
            if result.endswith("0"):
                raise HTTPException(status_code=404, detail="User not found")
            return {"detail": "User updated successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")


@user_router.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    db_pool: asyncpg.Pool = Depends(get_postgres),
):
    query = f"""
    delete from users where id = {user_id};
    """
    try:
        async with db_pool.acquire() as conn:
            result = await conn.execute(query)
            if result.endswith("0"):
                raise HTTPException(status_code=500, detail="User not found")
            return {"detail": "User deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete user")
