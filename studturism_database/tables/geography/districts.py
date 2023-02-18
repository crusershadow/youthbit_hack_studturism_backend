from .._studturism_meta import studturism_meta, Column, Table, sa_types
from .._schemas import Schemas

# Округ (ДФО, ЦФО)
districts = Table(
    'districts', studturism_meta,
    Column('district_id', sa_types.INTEGER, autoincrement=True, primary_key=True),
    Column('district_name', sa_types.TEXT, nullable=False, unique=True),
    # schema=Schemas.geography.name
)
