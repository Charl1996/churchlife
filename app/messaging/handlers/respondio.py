import re

from app.messaging.handlers.base_handler import BaseMessengerHandler
from app.requests import (
    get_request,
    post_request,
)
from configs import (
    RESPONDIO_BASE_URL,
    RESPONDIO_API_KEY,
)
from app.messaging.handlers.exceptions import (
    RespondIOInvalidPhoneNumberError,
    RespondIOFailedToRetrieveContactError,
    RespondIOFailedToSendMessageError,
)


class RespondIOUtils:

    @classmethod
    def valid_respondio_number(cls, number):
        return number.startswith('27') and len(number) == 11

    @classmethod
    def sanitize_mobile_number(cls, number):
        stripped_number = re.sub(r'[ +()-]', '', number)

        if cls.valid_respondio_number(stripped_number):
            return stripped_number
        if stripped_number.startswith('0') and len(stripped_number) == 10:
            return f'27{stripped_number[1:]}'
        raise RespondIOInvalidPhoneNumberError(f'{number} is not a valid respond.io phone number')


class RespondIOEndpoints:

    @classmethod
    def send_text_message_endpoint(cls, contact_id):
        return f"/message/sendContent/{contact_id}"

    @classmethod
    def get_contact_endpoint(cls, phone_number):
        return f"/contact/by_custom_field?name=phone&value={phone_number}"


class RespondIOHandler(BaseMessengerHandler):

    def __init__(self):
        super().__init__(
            url=RESPONDIO_BASE_URL,
            api_key=RESPONDIO_API_KEY,
        )

    def send_text_message(self, mobile_number, message, **kwargs):
        if not RespondIOUtils.valid_respondio_number(mobile_number):
            mobile_number = RespondIOUtils.sanitize_mobile_number(mobile_number)

        data = {
            'body': [{
                'type': 'text',
                'text': message,
            }]
        }

        status_code, content = post_request(
            RespondIOEndpoints.send_text_message_endpoint(mobile_number),
            data,
            self.request_headers(),
        )

        if status_code != 200:
            if self._contact_does_not_exist_error(status_code, content):
                _contact = self.create_contact(mobile_number, **kwargs)
                self.send_text_message(mobile_number, message)
            else:
                raise RespondIOFailedToSendMessageError

    def get_contact(self, mobile_number):
        if not RespondIOUtils.valid_respondio_number(mobile_number):
            mobile_number = RespondIOUtils.sanitize_mobile_number(mobile_number)

        status_code, content = get_request(
            RespondIOEndpoints.get_contact_endpoint(mobile_number),
            self.request_headers(),
        )

        if status_code != 200:
            raise RespondIOFailedToRetrieveContactError

        # Need to parse to format
        return content

    def create_contact(self, mobile_number, **kwargs):
        # Need to parse to format
        return {}

    def request_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_api_key()}'
        }

    def _contact_does_not_exist_error(self, status_code, content):
        return status_code == 403 and 'no such contact' in content.get('message')
