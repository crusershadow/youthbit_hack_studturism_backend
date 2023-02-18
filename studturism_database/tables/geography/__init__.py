from .districts import districts
from .regions import regions
from .cities import cities

from .._schemas import Schemas

for table in (districts, regions, cities):
    table.schema = Schemas.geography.name