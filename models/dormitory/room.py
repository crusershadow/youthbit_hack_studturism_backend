from typing import Tuple
from pydantic import BaseModel

class RoomCreate(BaseModel):
    type: str  # тип комнаты (1 местный / 2 местный и тд.)
    amount: int  # кол-во комнат такого типа
    description: str = None
    photos: Tuple[str, ...]
    price: int

class Room(BaseModel):
    room_id: str



