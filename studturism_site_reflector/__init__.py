import asyncio

from pprint import pprint
from typing import Dict, List, Iterable

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine

# region Models
from models.geography import District, DistrictCreate, RegionCreate, Region, CityCreate, City
from models.university import UniversityCreate, University
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
                city_id=cities_names_to_ids[u.details.city], name=u.details.name,
                admin_contacts=u.details.admin_contacts, photo_link=u.details.photo, site=u.details.site,
                committee=u.details.committee
            ) for u in universities
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

    async def reflect(self):
        api_universities: List[UniversityAPIModel] = await self.__api_client.get_all_universities()
        pprint(api_universities)
        districts: List[District] = await self.__reflect_districts(self.__make_districts(api_universities))
        regions: List[Region] = await self.__reflect_regions(self.__make_regions({d.district_name: d.district_id for d in districts}, api_universities))
        cities: List[City] = await self.__reflect_cities(self.__make_cities({r.region_name: r.region_id for r in regions}, api_universities))

        universities: List[University] = await self.__reflect_universities(
            self.__make_universities({c.city_name: c.city_id for c in cities}, api_universities)
        )
        pprint(universities)



        # districts = await self.__reflect_districts(districts=self.__make_districts_from_universities(universities))
        # print(districts)


async def main():
    a_engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/studturism')
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/studturism')
    s = StudturismSiteReflector(studturism_database=StudturismDatabase(async_engine=a_engine, sync_engine=engine))
    await s.reflect()
    return



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())