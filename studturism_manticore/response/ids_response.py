from typing import Any, List, Dict
from pydantic import BaseModel


class ManticoreIdsResponse(BaseModel):
    index_name: str
    ids: List[str]
    count: int

    @classmethod
    def from_json(cls, index_name: str, json_response: Dict[str, Any]):
        """
        Json ответ от Manticore имеет следующие поля:
            - data: сами данные
            - total: кол-во элементов в этом ответе
            - error:
            - warning:
        В этом ответе подразумевается наличие всего двух полей - ['id', 'highlight()']
        :param index_name:
        :param json_response:
        :return:
        """
        def is_json_response_empty(_json_response: Dict[str, Any]):
            return bool(int(_json_response['total']))

        if is_json_response_empty(json_response):
            raise ValueError('json_response is empty')
        return cls(
            index_name=index_name,
            count=json_response['total'],
            ids_highlight=[d['id'] for d in json_response['data']]
        )
