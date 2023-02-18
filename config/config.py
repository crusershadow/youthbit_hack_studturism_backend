import orjson

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from pydantic import BaseModel


class PostgreSQLConfig(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    sync_engine: Engine
    async_engine: AsyncEngine

    @classmethod
    def from_json_config(cls, config_path: str):
        with open(config_path, mode='r', encoding='utf-8') as file:
            postgresql_config_dict = orjson.loads(file.read())
        return PostgreSQLConfig(sync_engine=create_engine(postgresql_config_dict['sync_engine']),
                                async_engine=create_async_engine(postgresql_config_dict['async_engine']))

