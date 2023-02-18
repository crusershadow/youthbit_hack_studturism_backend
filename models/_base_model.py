from abc import abstractmethod
from pydantic import BaseModel as _BaseModel


class BaseStudturismModel(_BaseModel):

    @property
    @abstractmethod
    def id(self):
        return
