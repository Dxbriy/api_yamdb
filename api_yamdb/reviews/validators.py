import datetime

from rest_framework.exceptions import ValidationError


def year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            f'Некорректное значение года: {value}, '
            'не может быть больше текущего.',
            params={'value': value},
        )
    if value < 0:
        raise ValidationError(
            f'Некорректное значение года: {value}, '
            'не может быть отрицательным.',
            params={'value': value},
        )
