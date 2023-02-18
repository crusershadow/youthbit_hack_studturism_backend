from ._base_exc import BaseStudturismDatabaseError

class EntityAlreadyExistsError(BaseStudturismDatabaseError):

    def __init__(self, entity_model: 'pydantic.BaseModel'):
        self._model = entity_model

    def __str__(self):
        return f'Entity: {repr(self._model)} is already exists'
