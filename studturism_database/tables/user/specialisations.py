from studturism_database.tables._studturism_meta import studturism_meta, Table, Column, sa_types

specialisations = Table(
    'specialisations', studturism_meta,
    Column('spec_id', sa_types.SMALLINT, primary_key=True, autoincrement=True),
    Column('spec_name', sa_types.TEXT, nullable=False),
)
