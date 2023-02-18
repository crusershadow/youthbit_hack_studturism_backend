class ObjectNotFoundError(Exception):
    pass

class RoomNotFoundError(ObjectNotFoundError):
    pass

class DormitoryNotFoundError(ObjectNotFoundError):
    pass

class UniversityNotFoundError(ObjectNotFoundError):
    pass