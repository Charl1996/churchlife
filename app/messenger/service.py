from handlers import RespondIO
from configs import DEFAULT_MESSENGER_HANDLER

HANDLERS = {
    'respondio': RespondIO,
}


# This class is the "public" facing class that will be used to send messages
class MessengerService:

    handler: str

    def __init__(self, handler: str):
        self.handler = self.get_handler(handler)

    def get_handler(self, handler=DEFAULT_MESSENGER_HANDLER):
        return HANDLERS[handler]()

    def send_message(self, mobile_number, message):
        self.handler.send_message(mobile_number, message)
