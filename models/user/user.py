from datetime import date
from typing import Optional
from pydantic import Field, BaseModel

from datetime import date




class UserCreate(BaseModel):
    email: str
    password: str


class User(BaseModel):
    user_id: int
    email: str
    password_hash: str
    first_name: str = None
    middle_name: str = None
    last_name: str = None
    gender: str = None
    registration_date: date
    is_public: bool
