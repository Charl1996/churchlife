from app.requests import (
    get_request,
    post_request,
)
from configs import RESPONDIO_API_KEY
from app.messaging.handlers.respondio.exceptions import *
from app.messaging.handlers.respondio.helper import (
    RespondIOEndpoints,
    PayloadParser,
    WIX_PURCHASE_TEMPLATE,
    WIX_PURCHASE_TAGS,
)
from app.messaging.handlers.respondio.utils import (
    valid_respondio_number,
    sanitize_mobile_number,
)
from logger import logger


class RespondIORequest(RespondIOEndpoints, PayloadParser):

    def request_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {RESPONDIO_API_KEY}'
        }

    def contact_does_not_exist_error(self, status_code, content):
        return status_code == 403 and 'no such contact' in content.get('message')


class ContactsAPI(RespondIORequest):
    MAX_UPDATEABLE_TAGS = 10

    def get_contact(self, mobile_number):
        status_code, content = get_request(
            url=self.get_contact_endpoint(mobile_number),
            headers=self.request_headers(),
        )

        if status_code != 200:
            raise RespondIOFailedToRetrieveContactError

        # Need to parse to format to application common format?
        return content

    def add_contact_tags(self, contact_id, tags):
        tags_to_update = [tags]

        # Only MAX_UPDATEABLE_TAGS is allowed to be updated during one
        # API call :(
        if len(tags) > self.MAX_UPDATEABLE_TAGS:
            # Divide list of tags into groups of size MAX_UPDATEABLE_TAGS
            tags_to_update = [
                tags[i:i + self.MAX_UPDATEABLE_TAGS]
                for i in range(0, len(tags), self.MAX_UPDATEABLE_TAGS)
            ]

        for tags_partition in tags_to_update:
            data = self.parse_add_tags_data(tags_partition)

            status_code, content = post_request(
                url=self.add_tags_endpoint(contact_id),
                data=data,
                headers=self.request_headers()
            )

            if status_code != 200:
                raise RespondIOFailedToUpdateError(f"Could not update tags: {tags_partition}")

    def create_contact(self, data):
        parsed_data = self.parse_create_contact_data(data)

        status_code, content = post_request(
            url=self.create_contact_endpoint(),
            data=parsed_data,
            headers=self.request_headers(),
        )

        if status_code != 200:
            raise RespondIOFailedToRetrieveContactError

        # Need to parse to format to application common format?
        return content


class MessagesAPI(RespondIORequest):

    def send_template_message(self, mobile_number, template, **kwargs):
        data = self.parse_template_message_data(template, **kwargs)

        # Hard override for now due to testing
        mobile_number = '27824991602'

        status_code, content = post_request(
            self.send_message_endpoint(mobile_number),
            data,
            self.request_headers(),
        )

        if status_code != 201:
            if self.contact_does_not_exist_error(status_code, content):
                raise RespondIOContactDoesNotExistError
            else:
                raise RespondIOFailedToSendMessageError


class RespondIOHandler(ContactsAPI, MessagesAPI):

    def __init__(self):
        super().__init__()

    def send_wix_purchase_message(self, mobile_number, **kwargs):
        logger.info(f'RespondIOHandler send_wix_purchase_message: {mobile_number}')
        if not valid_respondio_number(mobile_number):
            mobile_number = sanitize_mobile_number(mobile_number)

        try:
            self.send_message(mobile_number, template=WIX_PURCHASE_TEMPLATE, **kwargs)
        except RespondIOContactDoesNotExistError as e:
            logger.error(f'RespondIOHandler send_wix_purchase_message: error => {e}')
            # Do with DataMapper or something like that...
            api_data = {
                'firstName': kwargs.get('first_name'),
                'lastName': kwargs.get('last_name'),
                'phone': mobile_number,
            }

            _contact = self.create_contact(api_data)
            logger.info(f'RespondIOHandler send_wix_purchase_message: trying again')
            self.send_message(mobile_number, template=WIX_PURCHASE_TEMPLATE, **kwargs)

        self.add_contact_tags(mobile_number, WIX_PURCHASE_TAGS)

    def send_message(self, *args, **kwargs):
        if 'template' in kwargs:
            self.send_template_message(*args, **kwargs)
