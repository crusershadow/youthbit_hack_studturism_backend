from .._studturism_meta import studturism_meta, Table, Column, ForeignKey, sa_types
from .._schemas import Schemas
from .regions import regions


cities = Table(
    'cities', studturism_meta,
    Column('city_id', sa_types.INTEGER, autoincrement=True, primary_key=True),
    Column('region_id', sa_types.SMALLINT, ForeignKey(f'{regions.fullname}.{regions.c.region_id.name}')),
    Column('city_name', sa_types.TEXT, nullable=False, unique=True),
    # schema=Schemas.geography.name
)
