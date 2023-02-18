from typing import Tuple
from pydantic import BaseModel


class Room(BaseModel):

    id: str
    type: str  # тип комнаты (1 местный / 2 местный и тд.)
    amount: int  # кол-во комнат такого типа
    description: str = None
    photos: Tuple[str, ...]
    price: int


