from app.messaging.handlers import RespondIO
from configs import DEFAULT_MESSENGER_HANDLER
from app.messaging.tasks import send_text_message_with_handler


HANDLERS = {
    'respondio': RespondIO,
}


class MessagingService:
    """
    This is the 'public' facing class that should be used to send
    any messages.
    """
    handler: object

    def __init__(self, handler: str):
        self.handler = self.get_handler(handler)

    def get_handler(self, handler=DEFAULT_MESSENGER_HANDLER):
        return HANDLERS[handler]()

    def send_async_text_message(self, mobile_number, message):
        send_text_message_with_handler.delay(self.handler, mobile_number, message)

    def send_text_message(self, mobile_number, message):
        send_text_message_with_handler(self.handler, mobile_number, message)
