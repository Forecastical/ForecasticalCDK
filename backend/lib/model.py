from pydantic import BaseModel
from typing import Optional

"""Pydantic models for Handling User Input"""


class UserAuth(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    # Existing fields
    username: str
    password: str
    user_fname: str
    user_lname: str
    user_age: int
    home_lat: float
    home_lon: float
    use_celsius: bool
    user_alerts: bool
    # New fields
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    preferred_activities: Optional[list[str]] = None
    favorite_weather: Optional[str] = None
    notification_email: Optional[str] = None
    theme_preference: Optional[str] = "dark"


class UserUpdate(BaseModel):
    # Existing fields
    username: Optional[str] = None
    password: Optional[str] = None
    user_fname: Optional[str] = None
    user_lname: Optional[str] = None
    user_age: Optional[int] = None
    home_lat: Optional[float] = None
    home_lon: Optional[float] = None
    use_celsius: Optional[bool] = None
    user_alerts: Optional[bool] = None
    # New fields
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    preferred_activities: Optional[list[str]] = None
    favorite_weather: Optional[str] = None
    notification_email: Optional[str] = None
    theme_preference: Optional[str] = None

class CreateComment(BaseModel):
    user_id: int
    comment: str
    lat: float
    lon: float


class EditComment(BaseModel):
    user_id: Optional[int]
    comment: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
