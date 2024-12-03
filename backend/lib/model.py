from pydantic import BaseModel, Field
from typing import Optional, List

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
    # Existing fields with added validation
    username: Optional[str] = None
    password: Optional[str] = None
    user_fname: Optional[str] = Field(None, min_length=1)
    user_lname: Optional[str] = Field(None, min_length=1)
    user_age: Optional[int] = Field(None, ge=0)
    home_lat: Optional[float] = Field(None, ge=-90, le=90)
    home_lon: Optional[float] = Field(None, ge=-180, le=180)
    use_celsius: Optional[bool] = None
    user_alerts: Optional[bool] = None
    # New fields remain the same
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    preferred_activities: Optional[list[str]] = None
    favorite_weather: Optional[str] = None
    notification_email: Optional[str] = None
    theme_preference: Optional[str] = None

    class Config:
        extra = "forbid"  # Prevents additional fields not defined in the model

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
