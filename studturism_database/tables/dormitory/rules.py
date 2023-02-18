from sqlalchemy import Table, Column, UniqueConstraint, types as sa_types

from .._studturism_meta import studturism_meta


rules = Table(
    'rules', studturism_meta,
    Column('rule_id', sa_types.INTEGER, primary_key=True, autoincrement=True),
    Column('required_uni_documents', sa_types.TEXT, nullable=False),
    Column('required_student_documents', sa_types.TEXT, nullable=False),
    Column('committee_name', sa_types.TEXT, nullable=True),
    Column('committee_email', sa_types.TEXT, nullable=True),
    Column('committee_phone', sa_types.TEXT, nullable=True),
    UniqueConstraint('required_uni_documents', 'required_student_documents', 'committee_name', 'committee_email', 'committee_phone')
)
