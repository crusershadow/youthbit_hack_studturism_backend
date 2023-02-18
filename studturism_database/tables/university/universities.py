from sqlalchemy import Table, Column, ForeignKey, types as sa_types
from sqlalchemy.dialects.postgresql import BYTEA

from .._studturism_meta import studturism_meta
from .._schemas import Schemas
from ..geography.cities import cities


universities = Table(
    'universities', studturism_meta,
    Column('uni_id', sa_types.SMALLINT, primary_key=True, autoincrement=True),
    Column('city_id', sa_types.SMALLINT, ForeignKey(f'{cities.fullname}.{cities.c.city_id.name}')),
    Column('uni_name', sa_types.TEXT, nullable=False, unique=True),
    Column('uni_admin_contacts', sa_types.TEXT, nullable=False),
    Column('uni_photo_link', sa_types.TEXT, nullable=True, unique=True),
    Column('uni_site', sa_types.TEXT, nullable=True),
    Column('uni_committee', sa_types.TEXT, nullable=True),
)
