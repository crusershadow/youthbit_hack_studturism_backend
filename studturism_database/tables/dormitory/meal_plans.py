from sqlalchemy import Table, Column, types as sa_types

from .._studturism_meta import studturism_meta

meal_plans = Table(
    'meal_plans', studturism_meta,
    Column('meal_plan_id', sa_types.SMALLINT, primary_key=True),
    Column('meal_plan_name', sa_types.TEXT, nullable=False),
    schema='dormitory'
)