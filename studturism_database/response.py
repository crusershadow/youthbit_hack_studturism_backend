from typing import List
from pydantic import BaseModel


class DatabaseResponse(BaseModel):
    count: int = None
    data: List[BaseModel]

    def __init__(self, data: List[BaseModel], count: int = None):
        if count is None:
            count = len(data)
        super().__init__(data=data, count=count)
