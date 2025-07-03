from pydantic import BaseModel, Field, model_validator
from datetime import date, datetime
from typing import Optional, List
import json


# base model for the events (updating and adding data)
class Event(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    start_date: date
    end_date: date
    city: str = Field(..., max_length=100)
    province_id: int
    event_website: str = Field(..., max_length=1000)
    organizer: str = Field(..., max_length=100)
    active: bool = True
    map_link: Optional[str] = Field(None, max_length=1000)
    multi_day: bool = False


# base model for the events with the id (returning data)
class Event_id(BaseModel):
    id: int
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    start_date: date
    end_date: date
    city: str = Field(..., max_length=100)
    province_id: int
    event_website: str = Field(..., max_length=1000)
    organizer: str = Field(..., max_length=100)
    active: bool = True
    map_link: Optional[str] = Field(None, max_length=1000)
    multi_day: bool = False


class EventType(BaseModel):
    id: int
    type: str = Field(..., max_length=100)


class EventType_id(BaseModel):
    type: str = Field(..., max_length=100)


class Provice(BaseModel):
    id: int
    p_name: str = Field(..., max_length=100)


class JunctionTable(BaseModel):
    event_id: int
    event_type_id: int


class EventImage_id(BaseModel):
    event_id: int
    headline: bool = False
    url: str = Field(..., max_length=1000)


class EventDistance_id(BaseModel):
    event_id: int
    day: int
    distance: int


class ImageDisplay(BaseModel):
    url: str = Field(..., max_length=1000)
    headline: bool


class DayDistanceDisplay(BaseModel):
    day: int
    distance: int


class EventTypeDisplay(BaseModel):
    event_type: str = Field(..., max_length=1000)


class EventMainDisplay(BaseModel):
    id: int
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    start_date: date
    end_date: date
    city: str = Field(..., max_length=100)
    event_website: str = Field(..., max_length=1000)
    organizer: str = Field(..., max_length=100)
    active: bool = True
    map_link: Optional[str] = Field(None, max_length=1000)
    # allows for the data been returned from postgres as json to be added to the model
    images: List[ImageDisplay] = Field(default_factory=list)
    # allows for the data been returned from postgres as json to be added to the model
    day_distance: List[DayDistanceDisplay] = Field(default_factory=list)
    multi_day: bool = False
    # allows for the data been returned from postgres as json to be added to the model
    event_type: List[EventTypeDisplay] = Field(default_factory=list)
    p_name: str = Field(..., max_length=100)

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
        if isinstance(values.get("event_type"), str):
            try:
                values["event_type"] = json.loads(values["event_type"])
            except Exception:
                values["event_type"] = []
        return values


class ErrorCreate_id(BaseModel):
    id: int
    row_number: int
    error: str = Field(..., max_length=500)
    inserted: bool
    run_date: datetime


class ErrorCreate(BaseModel):
    row_number: int
    error: str = Field(..., max_length=500)
    inserted: bool
    run_date: datetime
