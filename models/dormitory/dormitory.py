from typing import Tuple

from pydantic import BaseModel


class DormitoryMain(BaseModel):
    id: str
    name: str
    city: str
    duration_of_stay: Tuple[int, int]  # продолжительность пребывания (мин. кол-во дней, макс. кол-во дней)
    university_name: str
    meal_plan: str
    photos: Tuple[str, ...]
    price_range: Tuple[str, str]  # минимальная / максимальная цена


class DormitoryAdditional(BaseModel):
    pass