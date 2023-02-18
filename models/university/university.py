from pydantic import BaseModel


class UniversityCreate(BaseModel):
    city_id: int
    name: str
    admin_contacts: str
    photo_link: str = None
    site: str = None
    committee: str = None


class University(UniversityCreate):
    uni_id: int


