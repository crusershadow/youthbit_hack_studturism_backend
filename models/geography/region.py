from pydantic import BaseModel


class RegionCreate(BaseModel):
    district_id: int
    region_name: str


class Region(RegionCreate):
    region_id: int

    @classmethod
    def from_region_create(cls, region_create: RegionCreate, region_id: int):
        return cls(district_id=region_create.district_id, region_name=region_create.region_name, region_id=region_id)
