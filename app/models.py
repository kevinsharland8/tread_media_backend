from pydantic import BaseModel, Field, HttpUrl, model_validator
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
import json


# base model for the events (updating and adding data)
class Event(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    start_date: date
    end_date: date
    city: str = Field(..., max_length=100)
    province: str = Field(..., max_length=100)
    event_website: Optional[HttpUrl] = Field(None, max_length=1000)
    organizer: str = Field(..., max_length=100)
    active: bool = True
    map_link: Optional[str] = Field(None, max_length=1000)
    event_type_id: int
    multi_day: bool = False


# base model for the events with the id (returning data)
class Event_id(BaseModel):
    id: int
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    start_date: date
    end_date: date
    city: str = Field(..., max_length=100)
    province: str = Field(..., max_length=100)
    event_website: Optional[HttpUrl] = Field(None, max_length=1000)
    organizer: str = Field(..., max_length=100)
    active: bool = True
    map_link: Optional[str] = Field(None, max_length=1000)
    event_type_id: int
    multi_day: bool = False


class EventType(BaseModel):
    id: int
    type: str = Field(..., max_length=100)


class EventType_id(BaseModel):
    type: str = Field(..., max_length=100)


class EventImage(BaseModel):
    id: int
    event_id: int
    headline: bool = False
    url: HttpUrl = Field(..., max_length=1000)


class EventImage_id(BaseModel):
    event_id: int
    headline: bool = False
    url: HttpUrl = Field(..., max_length=1000)


class EventDistance(BaseModel):
    id: int
    event_id: int
    day: int
    distance: int


class EventDistance_id(BaseModel):
    event_id: int
    day: int
    distance: int


class Image(BaseModel):
    url: HttpUrl
    headline: bool


class DayDistance(BaseModel):
    day: int
    distance: int


class EventMainDisplay(BaseModel):
    id: int
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    start_date: date
    end_date: date
    city: str = Field(..., max_length=100)
    province: str = Field(..., max_length=100)
    event_website: Optional[HttpUrl] = Field(None, max_length=1000)
    organizer: str = Field(..., max_length=100)
    active: bool = True
    map_link: Optional[str] = Field(None, max_length=1000)
    # allows for the data been returned from postgres as json to be added to the model
    images: List[Image] = Field(default_factory=list)
    # allows for the data been returned from postgres as json to be added to the model
    day_distance: List[DayDistance] = Field(default_factory=list)
    multi_day: bool = False

    # @model_validator is used to convert the json string into a list of dictionaries
    @model_validator(mode="before")
    def parse_json_fields(cls, values):
        if isinstance(values.get("images"), str):
            try:
                values["images"] = json.loads(values["images"])
            except Exception:
                values["images"] = []
        if isinstance(values.get("day_distance"), str):
            try:
                values["day_distance"] = json.loads(values["day_distance"])
            except Exception:
                values["day_distance"] = []
        return values


# base model for the users (updating and adding data)
class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    google_id: str
    created_at: datetime
    updated_at: datetime


# base model for the users with the id (returning data)
class User_id(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    google_id: str
    created_at: datetime
    updated_at: datetime


# base model for the distance (updateing and adding data)
class Distance(BaseModel):
    distance: Decimal


# base model for the distance with the id (return data)
class Distance_id(BaseModel):
    id: int
    distance: Decimal


# base model for the event images (updateing and adding data)
class Evnet_image(BaseModel):
    event_id: int
    headline: bool
    image_url: str


# base model for the event images with the id (return data)
class Evnet_image_id(BaseModel):
    id: int
    event_id: int
    headline: bool
    image_url: str


# base model for the event type (updateing and adding data)
class Event_type(BaseModel):
    event_name: str


# base model for the event type with the id (return data)
class Event_type_id(BaseModel):
    id: int
    event_name: str
