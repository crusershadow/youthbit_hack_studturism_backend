from typing import Iterable
from sqlalchemy import Table

from .geography import districts, regions, cities
from .user import users, achievements, achievements_to_users
from .university import universities
from .dormitory import dormitories, meal_plans, rules

from ._schemas import Schemas


def set_schema_for_table_group(schema_: Schemas, table_group_: Iterable[Table]):
    for table in table_group_:
        table.schema = schema_.name


table_groups = {
    Schemas.geography: (districts, regions, cities),
    Schemas.user: (users, achievements, achievements_to_users),
    Schemas.university: (universities,),
    Schemas.dormitory: (dormitories, meal_plans, rules)
}

for schema, table_group in table_groups.items():
    set_schema_for_table_group(schema, table_group)
