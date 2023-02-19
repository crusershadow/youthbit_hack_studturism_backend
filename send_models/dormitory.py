from typing import List
from pydantic import BaseModel


class DormitoryTitleInfo(BaseModel):
    dor_id: int
    meal_plan_name: str
    city_name: str
    dor_visit_min_max_days: List[int]
    dor_min_max_price: List[int]
    dor_photos_links: List[str]
