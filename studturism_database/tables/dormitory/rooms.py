from sqlalchemy import Table, Column, UniqueConstraint, ForeignKey, types as sa_types
from .._studturism_meta import studturism_meta

from .dormitories import dormitories

rooms = Table(
    'rooms', studturism_meta,
    Column('room_id', sa_types.INTEGER, primary_key=True, autoincrement=True),
    Column('dormitory_id', sa_types.INTEGER, ForeignKey(f'{dormitories.fullname}.{dormitories.c.dor_id.name}')),
    Column('room_name', sa_types.TEXT, nullable=False),
    Column('room_description', sa_types.TEXT, nullable=True, server_default=None),
    Column('room_price_per_day', sa_types.SMALLINT, nullable=False),
    Column('rooms_amount', sa_types.SMALLINT, nullable=False),
    Column('rooms_photos_link', sa_types.ARRAY(sa_types.TEXT), server_default=None)
)