import asyncpg
from typing import List, Callable, Any, Optional
from fastapi import HTTPException
from settings import (
    POSTGRES_PORT,
    POSTGRES_DATABASE,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
)
from settings import pg_pool_min_size, pg_pool_max_size


conn_pool: Optional[asyncpg.Pool] = None

# move to a secret file
user = POSTGRES_USER
database = POSTGRES_DATABASE
password = POSTGRES_PASSWORD
hostname = POSTGRES_HOST
port = POSTGRES_PORT

DATABASE_URL = f"postgres://{user}:{password}@{hostname}:{port}/{database}"


# start up postgres connections
async def init_postgres() -> None:
    global conn_pool
    try:
        print("Initializing PostgreSQL connection pool...")

        conn_pool = await asyncpg.create_pool(
            dsn=DATABASE_URL, min_size=pg_pool_min_size, max_size=pg_pool_max_size
        )
        print("PostgreSQL connection pool created successfully.")

    except Exception as e:
        print(f"Error initializing PostgreSQL connection pool: {e}")
        raise


# get the connection when it is needed
async def get_postgres() -> asyncpg.Pool:
    global conn_pool
    if conn_pool is None:
        print("Connection pool is not initialized.")
        raise ConnectionError("PostgreSQL connection pool is not initialized.")
    try:
        return conn_pool
    except Exception as e:
        print(f"Failed to return PostgreSQL connection pool: {e}")
        raise


# safely close the connections
async def close_postgres() -> None:
    global conn_pool
    if conn_pool is not None:
        try:
            print("Closing PostgreSQL connection pool...")
            await conn_pool.close()
            print("PostgreSQL connection pool closed successfully.")
        except Exception as e:
            print(f"Error closing PostgreSQL connection pool: {e}")
            raise
    else:
        print("PostgreSQL connection pool was not initialized.")


# generic function to return data from the database
async def fetch_with_error_handling(
    db_pool: asyncpg.Pool,
    query: str,
    query_filters: Optional[Any] = None,
    # the ... This means it accepts any number and types of arguments, when you pass in the pydantic model the data needs to conform to
    model: Callable[..., Any] = dict,
) -> List[Any]:
    try:
        async with db_pool.acquire() as conn:
            if query_filters:
                results = await conn.fetch(query, query_filters)
                # model(**dict(row)) unpacks the dict as model(key1=value1, key2=value2, ...), which is what Pydantic models expect
                # returns a single result
                return model(**dict(results[0]))
            else:
                results = await conn.fetch(query)
                # model(**dict(row)) unpacks the dict as model(key1=value1, key2=value2, ...), which is what Pydantic models expect
                return [model(**dict(row)) for row in results]
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")


# generic function to update data in the database
async def patch_with_error_handling(
    db_pool: asyncpg.Pool,
    query: str,
    query_filters: Any,
    # the ... This means it accepts any number and types of arguments
    model: Callable[..., Any] = dict,
):
    try:
        async with db_pool.acquire() as conn:
            # *query_filters means unpack the list
            results = await conn.execute(query, *query_filters)
            if results.endswith("0"):
                raise HTTPException(status_code=404, detail="ID not found for updating")
            return {"detail": "Updated successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update {e}")


# generic function to delete data from the database
async def delete_with_error_handling(
    db_pool: asyncpg.Pool,
    query: str,
    query_filters: int,
    # the ... This means it accepts any number and types of arguments, when you pass in the pydantic model the data needs to conform to
    model: Callable[..., Any] = dict,
):
    try:
        async with db_pool.acquire() as conn:
            results = await conn.execute(query, query_filters)
            _, count = results.split()
            if int(count) == 0:
                raise HTTPException(status_code=404, detail="ID not found for deleting")
            return {"detail": "Deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete {e}")


# generic function to insert data in the database
async def insert_with_error_handling(
    db_pool: asyncpg.Pool,
    query: str,
    query_filters: Any,
    # the ... This means it accepts any number and types of arguments, when you pass in the pydantic model the data needs to conform to
    model: Callable[..., Any] = dict,
):
    try:
        async with db_pool.acquire() as conn:
            # *query_filters means unpack the list
            results = await conn.fetchrow(query, *query_filters)
            if not results["id"] > 0:
                raise HTTPException(
                    status_code=500, detail="Data was not inserted correctly"
                )
            return {"detail": "Inserted successfully", "result": results["id"]}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert {e}")
