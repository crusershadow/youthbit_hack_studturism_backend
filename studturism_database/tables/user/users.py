from studturism_database.tables._studturism_meta import studturism_meta
from sqlalchemy import Table, Column, types as sa_types
from sqlalchemy.sql.functions import now


users = Table(
    'users', studturism_meta,
    Column('user_id', sa_types.INTEGER, primary_key=True, autoincrement=True),
    Column('email', sa_types.TEXT, unique=True, nullable=False),
    Column('password_hash', sa_types.TEXT, nullable=False),
    Column('first_name', sa_types.TEXT, nullable=True, server_default=None),
    Column('middle_name', sa_types.TEXT, nullable=True, server_default=None),
    Column('last_name', sa_types.TEXT, nullable=True, server_default=None),
    Column('gender', sa_types.VARCHAR(1), nullable=True, server_default=None),
    Column('registration_date', sa_types.DATE, nullable=False, server_default=now()),
    Column('is_public', sa_types.BOOLEAN, nullable=False, server_default='true'),
)