from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, types as sa_types

from .._studturism_meta import studturism_meta
from .users import users
from .achievements import achievements

achievements_to_users = Table(
    'achievements_to_users', studturism_meta,
    Column(users.c.user_id.name, sa_types.INTEGER, ForeignKey(f'{users.fullname}.{users.c.user_id.name}'), nullable=False, unique=False),
    Column(achievements.c.achievement_id.name, sa_types.SMALLINT, ForeignKey(f'{achievements.fullname}.{achievements.c.achievement_id.name}'), nullable=False, unique=False),
    UniqueConstraint(users.c.user_id.name, achievements.c.achievement_id.name, name='user_achievement_uix')
)