from datetime import datetime
from typing import Union, List, Tuple, Dict

from pydantic import BaseModel, Field, validator

from .room import Room


class DormitoryCoordinates(BaseModel):
    lat: float
    lng: float


class DormitoryMainInfo(BaseModel):
    name: str
    city: str
    street: str
    house_number: str = Field(alias='houseNumber')
    coordinates: DormitoryCoordinates
    min_days: int = Field(alias='minDays')
    max_days: int = Field(alias='maxDays')
    photos: Tuple[str, ...]
    meal_plan: str = Field(alias='mealPlan')


class DormitoryCommittee(BaseModel):
    email: str = None
    phone: str = None
    name: str = None


class DormitoryRules(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    required_uni_document: str = Field(alias='requiredUniDocuments')
    required_students_documents: str = Field(alias='requiredStudentsDocuments')
    committee: DormitoryCommittee


class DormitoryService(BaseModel):
    id: str
    name: str
    price: int
    description: str = None
    is_free: bool = Field(alias='isFree')


class DormitoryDetails(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    main_info: DormitoryMainInfo = Field(alias='main-info')
    rules: DormitoryRules = None
    services: Tuple[DormitoryService, ...] = Field(default=tuple())
    documents: Tuple[str, ...] = Field(default=tuple())


class Dormitory(BaseModel):

    class Config:
        arbitrary_types_allowed = True
        extra = 'ignore'

    id: str
    user_id: str = Field(alias='userId')
    university_id: str = Field(alias='universityId')
    details: DormitoryDetails
    rooms: Dict[str, Room]
    on_moderation: bool = Field(alias='onModeration')




