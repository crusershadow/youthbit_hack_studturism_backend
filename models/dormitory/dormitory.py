from typing import Tuple, List

from pydantic import BaseModel


class DormitoryCreate(BaseModel):
    university_id: int
    meal_plan_id: int
    rule_id: int = None
    dor_name: str
    dor_street_name: str
    dor_street_house_number: str
    dor_lat: float
    dor_lng: float
    dor_visit_min_max_days: List[int]
    dor_photos_links: List[str] = None
    dor_documents_links: List[str] = None


class Dormitory(DormitoryCreate):
    dor_id: int
