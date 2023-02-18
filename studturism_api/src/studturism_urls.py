from functools import partial


def _concat_urls(*urls):
    return '/'.join(urls)


class _StudturismAPIURLS:

    __base_url = 'https://stud-api.sabir.pro'

    __dormitories = 'dormitories'
    __universities = 'universities'
    __rooms = 'rooms'

    __base_url_concat = partial(_concat_urls, __base_url)

    full_universities_all_url = __base_url_concat(__universities, 'all')
    full_dormitories_all_url = __base_url_concat(__dormitories, 'all')
    full_rooms_all_url = __base_url_concat(__rooms, 'all')

    @classmethod
    def full_url_room_with_id(cls, room_id: str):
        return cls.__base_url_concat(cls.__rooms, room_id)

    @classmethod
    def full_url_dormitory_with_id(cls, dormitory_id: str):
        return cls.__base_url_concat(cls.__dormitories, dormitory_id)

    @classmethod
    def full_url_university_with_id(cls, university_id: str):
        return cls.__base_url_concat(cls.__universities, university_id)