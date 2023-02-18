from pydantic import BaseModel, Field


class UniversityCreate(BaseModel):
    city_id: int
    uni_name: str #= Field(alias='uni_name')
    uni_admin_contacts: str #= Field(alias='uni_admin_contacts')
    uni_photo_link: str = None # Field(None, alias='uni_photo_link')
    uni_site: str = None # Field(None, alias='uni_site')
    uni_committee: str = None #Field(None, alias='uni_committee')


class University(UniversityCreate):
    uni_id: int


