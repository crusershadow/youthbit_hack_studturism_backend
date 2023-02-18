from typing import Tuple
from pydantic import BaseModel, Field, validator


class RoomDetails(BaseModel):
    is_free: bool = Field(alias='isFree')
    type: str # 1-но местный номер / 2 местный и тд
    description: str = None
    photos: Tuple[str, ...]
    amount: int
    price: int


class Room(BaseModel):

    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'

    id: str
    details: RoomDetails
    dormitory_id: str = Field(alias='dormitoryId')
    user_id: str = Field(alias='userId')
    university_id: str = Field(alias='universityId')
    on_moderation: bool = Field(alias='onModeration', default=None)
