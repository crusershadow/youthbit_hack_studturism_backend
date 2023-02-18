from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, types as sa_types

from .._studturism_meta import studturism_meta
from ..university import universities
from .meal_plans import meal_plans
from .rules import rules

dormitories = Table(
    'dormitories', studturism_meta,
    Column('dor_id', sa_types.INTEGER, primary_key=True, autoincrement=True),
    Column('university_id', sa_types.SMALLINT, ForeignKey(f'{universities.fullname}.{universities.c.uni_id.name}')),
    Column('meal_plan_id', sa_types.SMALLINT, ForeignKey(f'{meal_plans.fullname}.{meal_plans.c.meal_plan_id.name}')),
    Column('rule_id', sa_types.SMALLINT, ForeignKey(f'{rules.fullname}.{rules.c.rule_id.name}'), nullable=True),  # for first time nullable=True
    Column('dor_name', sa_types.TEXT, nullable=False),
    Column('dor_street_name', sa_types.TEXT, nullable=False),
    Column('dor_street_house_number', sa_types.TEXT, nullable=False),
    Column('dor_visit_min_max_days', sa_types.ARRAY(sa_types.SMALLINT), nullable=True),
    Column('dor_lat', sa_types.DOUBLE_PRECISION, nullable=False),
    Column('dor_lng', sa_types.DOUBLE_PRECISION, nullable=False),
    Column('dor_photos_links', sa_types.ARRAY(sa_types.TEXT), nullable=True),
    Column('dor_documents_links', sa_types.ARRAY(sa_types.TEXT), nullable=True),
    UniqueConstraint('university_id', 'dor_name', 'dor_street_name', 'dor_street_house_number')
)

