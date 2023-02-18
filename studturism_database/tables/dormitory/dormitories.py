from sqlalchemy import Table, Column, ForeignKey, types as sa_types

from .._studturism_meta import studturism_meta
from ..university import universities
from .meal_plans import meal_plans
from .rules import rules

dormitories = Table(
    'dormitories', studturism_meta,
    Column('dor_id', sa_types.INTEGER, primary_key=True, autoincrement=True),
    Column('university_id', sa_types.SMALLINT, ForeignKey(f'{universities.fullname}.{universities.c.uni_id.name}')),
    Column('meal_plan_id', sa_types.SMALLINT, ForeignKey(f'{meal_plans.fullname}.{meal_plans.c.meal_plan_id.name}')),
    Column('rule_id', sa_types.SMALLINT, ForeignKey(f'{rules.fullname}.{rules.c.rule_id.name}')),
    Column('dor_name', sa_types.TEXT, nullable=False),
    Column('dor_documents', sa_types.ARRAY(sa_types.TEXT), nullable=False),
    Column('dor_services_ids', sa_types.ARRAY(sa_types.INTEGER), nullable=True),
    Column('dor_rules_uni_documents', sa_types.TEXT, nullable=False),
    Column('dor_rules_student_documents', sa_types.TEXT, nullable=False),
    schema='dormitory'
)
