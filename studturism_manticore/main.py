import regex as re

from typing import List, Optional, Dict
from urllib.parse import quote_plus

from httpx import AsyncClient

from .response import ManticoreIdsResponse


class StudturismManticoreSearchEngine:

    __escaping_characters_finder = re.compile(r'[\\!"$\'\(\)\-/<@\^|~]')
    __sql_raw_manticore_mode_relative_url = '/sql?mode=raw'

    def __init__(self, manticore_http_server_url, universities_index_name: str, dormitories_index_name: str, cities_index_name: str, events_index_name: str):
        self.__url = manticore_http_server_url
        self.__client = AsyncClient(base_url=self.__url)

    def __prepare_query_string(self, query_string: str):
        new_query = query_string
        for character in (c_match.group(0) for c_match in self.__escaping_characters_finder.finditer(query_string)):
            new_query = new_query.replace(character, fr'\\{character}')
        return new_query

    def __make_select_id_match_query(self, index_name: str, query: str):
        return f"select id from {index_name} where match('{self.__prepare_query_string(query)}')"

    def _match_id_highlight(self, index_name: str, query: str) -> Optional[ManticoreIdsResponse]:
        try:
            response = await self.__client.post(
                self.__sql_raw_manticore_mode_relative_url,
                data={
                    'query': quote_plus(self.__make_select_id_match_query(index_name=index_name, query=query))
                }
            )
            response.raise_for_status()
        except Exception as err:
            raise err
        else:
            json_response = response.json()
            print(json_response)
            return ManticoreIdsResponse.from_json(index_name=index_name, json_response=json_response)

    async def search_universities(self, query: str):
        response = self._match_id_highlight()

    async def search_dormitories(self, query: str):
        pass

    async def search_cities(self, query: str):
        pass