
class BaseMessengerHandler:

    service_url: str
    service_api_key: str

    def __init__(self, url: str, api_key: str):
        self.service_url = url
        self.service_api_key = api_key

    def send_message(self, *args, **kwargs):
        raise NotImplementedError

    def get_contact(self, *args, **kwargs):
        raise NotImplementedError

    def get_contacts(self, *args, **kwargs):
        raise NotImplementedError

    def create_contact(self, *args, **kwargs):
        raise NotImplementedError

    def request_headers(self):
        raise NotImplementedError

    def get_api_key(self):
        return self.service_api_key

    def get_base_url(self):
        return self.service_url
