from typing import Optional, Type, Tuple, Dict, Iterable, Union, Any, List

from pprint import pprint
from pydantic import BaseModel
from loguru import logger

from sqlalchemy import MetaData, Table, Column
from sqlalchemy.engine import Engine
from sqlalchemy.sql import select, insert, update, delete, join, bindparam, text, any_
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.sql.expression import any_
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, AsyncResult, AsyncMappingResult
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from asyncpg.exceptions import UniqueViolationError

# region Tables
from .tables._studturism_meta import studturism_meta
from .tables.geography import districts, regions, cities
from .tables.university import universities
from .tables.dormitory import dormitories, meal_plans, rules, rooms
from .tables.user import users
from .tables import Schemas
# endregion

# region Models
from models.geography.district import DistrictCreate, District
from models.geography.region import RegionCreate, Region
from models.geography.city import CityCreate, City

from models.dormitory.dormitory import DormitoryCreate, Dormitory
from models.dormitory.room import RoomCreate, Room
from models.dormitory.rules import RuleCreate, Rule
from models.dormitory.meal_plan import MealPlanCreate, MealPlan

from models.university import UniversityCreate, University

from models.user import UserCreate, User
# endregion

# region SendModels
from send_models.dormitory import DormitoryTitleInfo
# endregion

from .response import DatabaseResponse

# region Errors
from .exc import BaseStudturismDatabaseError, EntityAlreadyExistsError
# endregion

class _PreparedSQLStatements:

    @staticmethod
    def generate_inserting_bind_params(
            table: Table,
            remove_prefix_value: Optional[str] = None,
            exclude_primary_keys: bool = True
    ):
        return {
            c.name:
                bindparam(c.name.lstrip(remove_prefix_value))
                if remove_prefix_value is not None else bindparam(c.name)
            for c in table.c if exclude_primary_keys is False or c.primary_key is False
        }

    insert_district_returning_id_stmt = insert(districts).values(
        generate_inserting_bind_params(districts, remove_prefix_value='district_', exclude_primary_keys=True)
    ).returning(districts.c.district_id)

    insert_user_returning_id_stmt = insert(users).values(
        generate_inserting_bind_params(users, remove_prefix_value=None, exclude_primary_keys=True)
    ).returning(users.c.user_id)

    insert_university_returning_id_stmt = insert(universities).values(
        **generate_inserting_bind_params(universities, 'uni_', exclude_primary_keys=True)
    ).returning(universities.c.uni_id)

    insert_dormitory_returning_id_stmt = insert(dormitories).values(
        **generate_inserting_bind_params(dormitories, 'dor_', exclude_primary_keys=True)
    ).returning(dormitories.c.dor_id)

    @staticmethod
    def generate_select_all_columns_stmt(table: Table, where_condition_columns: Iterable, limit: int = 50):
        return select(table).where(*where_condition_columns).limit(limit)


class StudturismDatabase:

    def __init__(self, async_engine: AsyncEngine, sync_engine: Engine, *, reset_database_: bool = False):
        self.__async_engine = async_engine
        self.__sync_engine = sync_engine

        self.__meta: MetaData = studturism_meta
        if reset_database_ is True:
            self.__meta.drop_all(bind=self.__sync_engine)
            logger.info('Database was dropped')

        logger.debug('Setting up database...')
        self.__create_schemas()
        logger.debug('Schemas initialized')
        self.__meta.create_all(bind=self.__sync_engine)
        logger.debug('Database was successfully set up')

    # region Other
    def __create_schemas(self):
        from sqlalchemy.schema import CreateSchema
        with self.__sync_engine.connect() as conn:
            for schema in Schemas:
                conn.execute(CreateSchema(schema.name, if_not_exists=True))
            conn.commit()
    # endregion

    # region Statements Execution
    async def __insert(self, insert_stmt, params: Union[Dict[str, Any], List[Dict[str, Any]]] = None):
        async with self.__async_engine.connect() as conn:
            try:
                result = await conn.execute(insert_stmt, params)
            except SQLAlchemyError as err:
                await conn.rollback()
                raise err
            else:
                await conn.commit()
                return result

    async def __select(self, select_stmt, params=None):
        async with self.__async_engine.connect() as conn:
            try:
                result = await conn.execute(select_stmt, params)
            except SQLAlchemyError as err:
                raise err
            else:
                return result

    async def __update(self, update_stmt: update):
        async with self.__async_engine.connect() as conn:
            try:
                result = await conn.execute(update_stmt)
            except SQLAlchemyError as err:
                await conn.rollback()
                raise err
            else:
                return result

    async def __delete(self, delete_stmt: delete):
        async with self.__async_engine.connect() as conn:
            try:
                result = await conn.execute(delete_stmt)
            except SQLAlchemyError as err:
                await conn.rollback()
                raise err
            else:
                return result
    # endregion

    # region Create
    async def __create_entity(
            self,
            inserting_stmt_with_bindparams,
            params: Dict[str, Any],
            full_entity_model,
            on_duplicating_select_stmt_with_bindparams: select = None,
    ):
        try:
            result = await self.__insert(inserting_stmt_with_bindparams, params)
        except IntegrityError as err:
            if on_duplicating_select_stmt_with_bindparams is None:
                raise EntityAlreadyExistsError(params)
            result = await self.__select(on_duplicating_select_stmt_with_bindparams, params)

        try:
            return full_entity_model(**params, **result.mappings().fetchone())
        except Exception as err:
            raise err


    async def create_district(self, district_create: DistrictCreate) -> District:
        return await self.__create_entity(
            insert(districts).values(district_name=bindparam('district_name')).returning(districts.c.district_id),
            district_create.dict(),
            District,
            select(districts.c.district_id).where(districts.c.district_name == bindparam('district_name'))
        )

    async def create_region(self, region_create: RegionCreate):
        return await self.__create_entity(
            insert(regions).values(region_name=bindparam('region_name')).returning(regions.c.region_id),
            region_create.dict(),
            Region,
            select(regions.c.region_id).where(regions.c.region_name == bindparam('region_name'))
        )

    async def create_city(self, city_create: CityCreate):
        return await self.__create_entity(
            insert(cities).values(city_name=bindparam('city_name'), region_id=bindparam('region_id')).returning(cities.c.city_id),
            city_create.dict(),
            City,
            select(cities.c.city_id).where(cities.c.city_name == bindparam('city_name'))
        )

    async def create_university(self, university_create: UniversityCreate):
        return await self.__create_entity(
            insert(universities).values(
                city_id=bindparam('city_id'),
                uni_name=bindparam('uni_name'),
                uni_admin_contacts=bindparam('uni_admin_contacts'),
                uni_photo_link=bindparam('uni_photo_link'),
                uni_site=bindparam('uni_site'),
                uni_committee=bindparam('uni_committee')
            ).returning(universities.c.uni_id),
            university_create.dict(),
            University,
            select(universities.c.uni_id).where(universities.c.uni_name == bindparam('uni_name')).limit(1)
        )

    async def create_meal_plan(self, meal_plan_create: MealPlanCreate) -> MealPlan:
        m_dict = meal_plan_create.dict()
        return await self.__create_entity(
            insert(meal_plans).values(meal_plan_name=bindparam('meal_plan_name')).returning(meal_plans.c.meal_plan_id),
            m_dict,
            MealPlan,
            select(meal_plans.c.meal_plan_id).where(meal_plans.c.meal_plan_name == bindparam('meal_plan_name'))
        )

    async def create_rule(self, rule_create: RuleCreate) -> Rule:
        return await self.__create_entity(
            insert(rules).values(
                required_uni_documents=bindparam('required_uni_documents'),
                required_student_documents=bindparam('required_student_documents'),
                committee_name=bindparam('committee_name'),
                committee_email=bindparam('committee_email'),
                committee_phone=bindparam('committee_phone')),
            rule_create.dict(),
            Rule,
            select(rules).where(
                required_uni_documents=bindparam('required_uni_documents'),
                required_student_documents=bindparam('required_student_documents'),
                committee_name=bindparam('committee_name'),
                committee_email=bindparam('committee_email'),
                committee_phone=bindparam('committee_phone'))
        )

    async def create_dormitory(self, dormitory_create: DormitoryCreate) -> Dormitory:
        return await self.__create_entity(
            insert(dormitories).values(
                university_id=bindparam('university_id'),
                meal_plan_id=bindparam('meal_plan_id'),
                rule_id=bindparam('rule_id'),
                dor_name=bindparam('dor_name'),
                dor_street_name=bindparam('dor_street_name'),
                dor_street_house_number=bindparam('dor_street_house_number'),
                dor_visit_min_max_days=bindparam('dor_visit_min_max_days'),
                dor_lat=bindparam('dor_lat'),
                dor_lng=bindparam('dor_lng'),
                dor_photos_links=bindparam('dor_photos_links'),
                dor_documents_links=bindparam('dor_documents_links'),
            ).returning(dormitories.c.dor_id),
            dormitory_create.dict(),
            Dormitory,
            select(dormitories.c.dor_id).where(
                dormitories.c.university_id == bindparam('university_id'),
                dormitories.c.dor_name == bindparam('dor_name')
            )
        )

    async def create_service(self):
        pass

    async def register_user(self, email: str, password_hash: str) -> User:
        """
        :param email:
        :param password_hash:
        :return: UserInDB
        :raises EntityAlreadyExistsError: если такой пользователь уже сушествует
        """
        return await self.__create_entity(
            insert(users).values(email=bindparam('email'), password_hash=bindparam('password_hash')).returning(users.c.user_id),
            params={'email': email, 'password_hash': password_hash},
            full_entity_model=User
        )

    # endregion

    # region Get
    @staticmethod
    def __generate_columns_equal_expressions(table, params: Dict[str, Any]):
        return (table.c[col_name] == value for col_name, value in params.items())

    async def __select_models_as_result(self, select_stmt, model_class: Type, ):
        result = (await self.__select(select_stmt)).mappings().fetchall()
        return DatabaseResponse([model_class(**row) for row in result])

    async def get_district(self, **districts_params) -> District:
        return await self.__select(select(districts).where())

    async def get_user(self, **users_params) -> User:
        result = await self.__select(select(users).where(*self.__generate_columns_equal_expressions(users, users_params)).limit(1))
        return User(**result.mappings().fetchone())

    async def get_universities(self) -> DatabaseResponse:
        return await self.__select_models_as_result(select(universities), University)

    async def get_dormitories(self) -> DatabaseResponse:
        return await self.__select_models_as_result(select(dormitories), Dormitory)

    async def get_dormitories_titles_info(self):
        result = await self.__select(
            select(dormitories.c.dor_id, dormitories.c.dor_visit_min_max_days, meal_plans.c.meal_plan_name, cities.c.city_name, )
        )

    async def get_dormitories_by_university_id(self, university_id: int) -> List[University]:
        return

    async def get_cities_by_id(self, *cities_ids: int):
        return await self.__select_models_as_result(select(cities).where(cities.c.city_id == any_(array(cities_ids))))

    async def get_cities(self):
        return await self.__select_models_as_result(select(cities), City)
    # endregion

    # def add_university\\\\\](self, University):
