from sqlalchemy import Table, Column, types as sa_types
from .._studturism_meta import studturism_meta

achievements = Table(
    'achievements', studturism_meta,
    Column('achievement_id', sa_types.SMALLINT, primary_key=True, autoincrement=True),
    Column('achievement_name', sa_types.TEXT, nullable=False),
    Column('achievement_description', sa_types.TEXT, nullable=False),
)