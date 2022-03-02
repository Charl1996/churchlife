from app.messenger.handlers.base_handler import BaseMessengerHandler
from app.requests import (
    post_request
)
from configs import (
    RESPONDIO_BASE_URL,
    RESPONDIO_API_KEY,
)

class RespondIOContact:
    id: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']


class RespondIOEndpoint:

    @classmethod
    def send_message(cls, contact_id):
        return f"/message/sendContent/{contact_id}"


class RespondIO(BaseMessengerHandler):

    def __init__(self):
        super().__init__(
            url=RESPONDIO_BASE_URL,
            api_key=RESPONDIO_API_KEY,
        )

    def send_message(self, mobile_number, message):
        data = {
            'type': 'text',
            'text': message
        }

        result = post_request(
            RespondIOEndpoint.send_message(mobile_number),
            data,
            self.request_headers(),
        )

        if result.status_code != 200:
            # Check for the error for when the contact is not found
            # i.e. create the contact and try again
            contact = self.create_contact(mobile_number)
            if not contact:
                self.send_message(mobile_number, message)

    def create_contact(self, mobile_number) -> RespondIOContact:
        return {}

    def get_contact(self, mobile_number) -> RespondIOContact:
        # If not contact exists, return None
        return False

    def request_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_api_key()}'
        }
