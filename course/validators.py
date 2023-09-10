from collections import OrderedDict

from rest_framework.serializers import ValidationError
from validators.url import url as is_url


class VideoURLValidator:

    def __init__(self, field_name: str):
        self.field_name = field_name

    def __call__(self, fields: OrderedDict) -> None:

        url = dict(fields).get(self.field_name)

        if url is not None and 'youtube.com' not in url:
            raise ValidationError('Не правильный url')


class IsURLValidator:

    def __call__(self, fields: OrderedDict) -> None:

        for field in fields.items():
            if is_url(field[1]):

                if field[0] == 'url':
                    continue

                raise ValidationError('''url должен быть в поле 'url'.''')