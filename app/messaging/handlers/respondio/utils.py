import re

from app.messaging.handlers.respondio.exceptions import (
    RespondIOInvalidPhoneNumberError,
)


def valid_respondio_number(cls, number):
    return number.startswith('27') and len(number) == 11


def sanitize_mobile_number(cls, number):
    stripped_number = re.sub(r'[ +()-]', '', number)

    if cls.valid_respondio_number(stripped_number):
        return stripped_number
    if stripped_number.startswith('0') and len(stripped_number) == 10:
        return f'27{stripped_number[1:]}'
    raise RespondIOInvalidPhoneNumberError(f'{number} is not a valid respond.io phone number')
