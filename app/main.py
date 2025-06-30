from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import init_postgres, close_postgres
from api.v1.route_events import event_router
from api.v1.route_upload import upload_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


# create asynchronous context managers
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_postgres()
    yield
    await close_postgres()


app: FastAPI = FastAPI(lifespan=lifespan, title="Tread Media Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://192.168.68.145:4200"],  # Or restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# adding the routs to the application
app.include_router(event_router)
# app.include_router(user_router)
app.include_router(upload_router)
# app.include_router(distance_router)
# app.include_router(event_type_router)


@app.get("/")
async def home():
    return {"status": "running"}

# starting up the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
