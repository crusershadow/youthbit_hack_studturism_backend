from pydantic import BaseModel


class CityCreate(BaseModel):
    region_id: int
    city_name: str


class City(CityCreate):
    city_id: int