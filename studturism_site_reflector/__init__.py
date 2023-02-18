import asyncio

from pprint import pprint
from typing import Dict, List, Iterable

from loguru import logger
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine

# region Models
from models.geography import District, DistrictCreate, RegionCreate, Region, CityCreate, City
from models.university import UniversityCreate, University
from models.dormitory import DormitoryCreate, Dormitory, RuleCreate, Rule, RoomCreate, Room, MealPlanCreate, MealPlan

# endregion

# region StudturismAPI
from studturism_api import StudturismAPI
from studturism_api.src.api_models import Dormitory as DormitoryAPIModel, University as UniversityAPIModel
# endregion

# region Database
from studturism_database import StudturismDatabase
from studturism_database.exc import EntityAlreadyExistsError
# endregion


class StudturismSiteReflector:

    def __init__(self, studturism_database: StudturismDatabase):
        self.__api_client = StudturismAPI()
        self.__database = studturism_database

    # region Models Makers
    @staticmethod
    def __make_districts(universities: Iterable[UniversityAPIModel]):
        return [DistrictCreate(district_name=d_name) for d_name in {uni.details.district for uni in universities}]

    @staticmethod
    def __make_regions(
            districts_names_to_ids: Dict[str, int],
            universities: Iterable[UniversityAPIModel],
    ) -> List[RegionCreate]:
        return [RegionCreate(region_name=uni.details.region, district_id=districts_names_to_ids[uni.details.district]) for uni in universities]

    @staticmethod
    def __make_cities(regions_names_to_ids: Dict[str, int], universities: Iterable[UniversityAPIModel]):
        return [CityCreate(city_name=uni.details.city, region_id=regions_names_to_ids[uni.details.region]) for uni in universities]

    @staticmethod
    def __make_universities(cities_names_to_ids: Dict[str, int], universities: Iterable[UniversityAPIModel]):
        return [
            UniversityCreate(
                city_id=cities_names_to_ids[u.details.city], uni_name=u.details.name,
                uni_admin_contacts=u.details.admin_contacts, uni_photo_link=u.details.photo, uni_site=u.details.site,
                uni_committee=u.details.committee
            ) for u in universities
        ]

    @staticmethod
    def __make_dormitories(universities_api_ids_to_db_ids: Dict[str, int], meal_plans_names_to_ids: Dict[str, int], dormitories: Iterable[DormitoryAPIModel]):
        return [
                DormitoryCreate(
                    university_id=universities_api_ids_to_db_ids[d.university_id],
                    meal_plan_id=meal_plans_names_to_ids[d.details.main_info.meal_plan],
                    rule_id=None,
                    dor_name=d.details.main_info.name,
                    dor_street_name=d.details.main_info.street,
                    dor_street_house_number=d.details.main_info.house_number,
                    dor_visit_min_max_days=[d.details.main_info.min_days, d.details.main_info.max_days],
                    dor_lat=d.details.main_info.coordinates.lat,
                    dor_lng=d.details.main_info.coordinates.lng,
                    dor_photos_links=d.details.main_info.photos,
                    dor_documents_links=d.details.documents
                ) for d in dormitories
            ]
    # endregion

    # region Reflect
    @staticmethod
    async def __reflect_base(creating_db_model_func, models_list):
        returning_list = []
        for model in models_list:
            created_model = await creating_db_model_func(model)
            returning_list.append(created_model)
        return returning_list

    async def __reflect_districts(self, districts: List[DistrictCreate]):
        return await self.__reflect_base(self.__database.create_district, districts)

    async def __reflect_regions(self, regions: List[RegionCreate]):
        return await self.__reflect_base(self.__database.create_region, regions)

    async def __reflect_cities(self, cities: List[CityCreate]):
        return await self.__reflect_base(self.__database.create_city, cities)

    async def __reflect_universities(self, universities: List[UniversityCreate]):
        return await self.__reflect_base(self.__database.create_university, universities)

    async def __reflect_meal_plans(self, meal_plans: List[MealPlanCreate]):
        return await self.__reflect_base(self.__database.create_meal_plan, meal_plans)

    async def __reflect_rules(self, rules: List[RuleCreate]):
        return await self.__reflect_base(self.__database.create_rule, rules)

    async def __reflect_dormitories(self, dormitories: List[DormitoryCreate]):
        return await self.__reflect_base(self.__database.create_dormitory, dormitories)

    async def _reflect_universities_part(self, universities_api_models: List[UniversityAPIModel]):
        districts: List[District] = await self.__reflect_districts(self.__make_districts(universities_api_models))
        regions: List[Region] = await self.__reflect_regions(self.__make_regions({d.district_name: d.district_id for d
                                                                                  in districts}, universities_api_models))
        cities: List[City] = await self.__reflect_cities(self.__make_cities({r.region_name: r.region_id for r in
                                                                             regions}, universities_api_models))
        universities: List[University] = await self.__reflect_universities(
            self.__make_universities({c.city_name: c.city_id for c in cities}, universities_api_models)
        )
        return universities

    async def _reflect_dormitories_part(self, universities_api_ids_to_universities_db_ids: Dict[str, int]):
        dormitories_api_models: List[DormitoryAPIModel] = list(filter(lambda dor: dor.university_id in universities_api_ids_to_universities_db_ids, await self.__api_client.get_all_dormitories()))
        meal_plans = await self.__reflect_meal_plans([MealPlanCreate(meal_plan_name=meal_plan) for meal_plan in {d.details.main_info.meal_plan for d in dormitories_api_models}])
        meals_plans_names_to_ids = {m.meal_plan_name: m.meal_plan_id for m in meal_plans}
        dormitories = await self.__reflect_dormitories(
            self.__make_dormitories(universities_api_ids_to_universities_db_ids, meals_plans_names_to_ids, dormitories_api_models)
        )
        return dormitories

    async def reflect(self):
        logger.info('Starting to reflect site')
        universities_api_models: List[UniversityAPIModel] = await self.__api_client.get_all_universities()
        universities = await self._reflect_universities_part(universities_api_models)
        universities_names: Dict[str, int] = {uni.uni_name: uni.uni_id for uni in universities}

        dormitories = await self._reflect_dormitories_part({uni.id: universities_names[uni.details.name] for uni in universities_api_models})
        # pprint(dormitories)
        logger.info('Site reflected')
        # districts = await self.__reflect_districts(districts=self.__make_districts_from_universities(universities))
        # print(districts)


async def main():
    from config.config import PostgreSQLConfig
    p_config = PostgreSQLConfig.from_json_config('../config/postgresql.json')
    s = StudturismSiteReflector(studturism_database=StudturismDatabase(
        async_engine=p_config.async_engine,
        sync_engine=p_config.sync_engine,
        reset_database_=True
    ))
    await s.reflect()
    return



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())