from fastapi import APIRouter, Depends, status
from models import ErrorCreate
from db import (
    get_postgres,
    fetch_with_error_handling,
)
from typing import List
import asyncpg

error_router = APIRouter(prefix="/error", tags=["error"])


@error_router.get("/", response_model=List[ErrorCreate], status_code=status.HTTP_200_OK)
async def error(
    db_pool: asyncpg.Pool = Depends(get_postgres),
) -> List[ErrorCreate]:
    query = "select row_number, error, inserted, max(run_date) run_date from errors group by row_number, error, inserted order by row_number;"
    return await fetch_with_error_handling(
        db_pool=db_pool, query=query, model=ErrorCreate
    )
