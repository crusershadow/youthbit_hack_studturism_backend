from pydantic import BaseModel, Field


class UniversityDetails(BaseModel):
    name: str
    district: str
    region: str
    city: str
    admin_contacts: str = Field(alias='adminContacts')
    photo: str = None
    site: str = None
    committee: str = None
    short_name: str = Field(alias='shortName', default=None)
    founder_name: str = Field(alias='founderName', default=None)


class University(BaseModel):
    id: str
    user_id: str = Field(alias='userId')
    on_moderation: bool = Field(alias='onModeration')
    details: UniversityDetails
