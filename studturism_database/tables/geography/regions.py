from sqlalchemy import Table, Column, ForeignKey, types as sa_types

from .._studturism_meta import studturism_meta
from .._schemas import Schemas
from .districts import districts

regions = Table(
    'regions', studturism_meta,
    Column('region_id', sa_types.INTEGER, primary_key=True, autoincrement=True),
    Column('district_id', sa_types.SMALLINT, ForeignKey(f'{districts.fullname}.{districts.c.district_id.name}')),
    Column('region_name', sa_types.TEXT, nullable=False, unique=True),
    # schema=Schemas.geography.name
)
