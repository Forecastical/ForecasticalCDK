from pydantic import BaseModel
from typing import Optional

"""Pydantic models for Handling User Input"""


class UserAuth(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    password: str
    user_fname: str
    user_lname: str
    user_age: int
    home_lat: float
    home_lon: float
    use_celsius: bool
    user_alerts: bool


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    user_fname: Optional[str]
    user_lname: Optional[str]
    user_age: Optional[int]
    home_lat: Optional[float]
    home_lon: Optional[float]
    use_celsius: Optional[bool]
    user_alerts: Optional[bool]


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
