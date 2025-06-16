from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

# base model for the events (updating and adding data)
class Event(BaseModel):
    event_name: str
    event_description: str
    start_date: datetime
    end_date: datetime
    province: str
    event_date: datetime
    event_website: str
    organizer: str
    active: bool
    headline_image: str
    promotion_images: str
    map_link: str

# base model for the events with the id (returning data)
class Event_id(BaseModel):
    id: int
    event_name: str
    event_description: str
    start_date: datetime
    end_date: datetime
    province: str
    event_date: datetime
    event_website: str
    organizer: str
    active: bool
    headline_image: str
    promotion_images: str
    map_link: str

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