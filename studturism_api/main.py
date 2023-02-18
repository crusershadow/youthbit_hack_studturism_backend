import asyncio
from pprint import pprint
from typing import List, Type, Union, Optional

from pydantic.error_wrappers import ValidationError
from httpx import AsyncClient
from studturism_api.src.studturism_urls import _StudturismAPIURLS

from studturism_api.src.api_models import Dormitory, University, Room


class StudturismAPI:

    def __init__(self):
        self.__client = AsyncClient()

    async def __get_response_as_model(self, model: Type[Union[Dormitory, University, Room]], url: str, **kwargs) -> Optional[Union[Dormitory, University, Room]]:
        r = await self.__client.get(url, **kwargs)
        if r.status_code == 404:
            return None

        return model(**r.json())

    async def __get_response_as_list_of_models(self, model: Type[Union[Dormitory, University, Room]], url: str, **kwargs) -> List[Union[Dormitory, University, Room]]:
        # return [model(**obj) for obj in (await self.__client.get(url, **kwargs)).json() if obj['onModeration'] is False]
        response = await self.__client.get(url, **kwargs)
        models_list = []
        for obj in response.json():
            if obj.get('onDebug'):
                continue
            try:
                models_list.append(model(**obj))
            except ValidationError:
                continue
            except Exception as err:
                raise err
        return models_list

    async def get_dormitory(self, dormitory_id: str) -> Dormitory:
        return await self.__get_response_as_model(Dormitory, _StudturismAPIURLS.full_url_dormitory_with_id(dormitory_id))

    async def get_all_dormitories(self) -> List[Dormitory]:
        return await self.__get_response_as_list_of_models(Dormitory, _StudturismAPIURLS.full_dormitories_all_url)

    async def get_university(self, university_id: str) -> University:
        return await self.__get_response_as_model(University, _StudturismAPIURLS.full_url_university_with_id(university_id))

    async def get_all_universities(self) -> List[University]:
        return await self.__get_response_as_list_of_models(University, _StudturismAPIURLS.full_universities_all_url)

    async def get_room(self, room_id: str) -> Room:
        return await self.__get_response_as_model(Room, _StudturismAPIURLS.full_url_room_with_id(room_id))

    async def get_all_rooms(self) -> List[Room]:
        return await self.__get_response_as_list_of_models(Room, _StudturismAPIURLS.full_rooms_all_url)


async def main():
    s = StudturismAPI()
    return await s.get_university(
        'faxkyrxypIxzvczxv'
    )
    # return await s.get_dormitory(dormitory_id='qab1lW4Acx')


if __name__ == '__main__':
    r = asyncio.run(main())

    from pprint import pprint
    pprint(r)