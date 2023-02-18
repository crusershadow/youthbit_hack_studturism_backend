from pydantic import BaseModel


class DistrictCreate(BaseModel):
    district_name: str


class District(DistrictCreate):
    district_id: int

