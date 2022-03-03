from app.messaging.handlers import RespondIOHandler
from configs import DEFAULT_MESSAGING_HANDLER
from app.messaging.tasks import send_wix_purchase_message_with_handler


HANDLERS = {
    'respondio': RespondIOHandler,
}


class MessagingService:
    """
    This is the 'public' facing class that should be used to send
    any messages.
    """
    handler: object

    def __init__(self, handler=DEFAULT_MESSAGING_HANDLER):
        self.handler = self.get_handler(handler)

    def get_handler(self, handler):
        return HANDLERS[handler]()

    def send_wix_purchase_message(self, mobile_number, **kwargs):
        send_wix_purchase_message_with_handler.delay(self.handler, mobile_number, **kwargs)
