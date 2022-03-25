from app.integrations.messaging.handlers import RespondIOHandler
from configs import DEFAULT_MESSAGING_HANDLER
from app.integrations.messaging.tasks import send_wix_purchase_message_with_handler


HANDLERS = {
    'respondio': RespondIOHandler,
}


class MessagingService:
    """
    This is the 'public' facing class that should be used to send
    any messages.
    """
    handler_slug: str

    def __init__(self, handler=DEFAULT_MESSAGING_HANDLER):
        self.handler_slug = handler

    @classmethod
    def get_handler_class(cls, handler):
        return HANDLERS[handler]()

    def send_wix_purchase_message(self, mobile_number, **kwargs):
        send_wix_purchase_message_with_handler.delay(self.handler_slug, mobile_number, **kwargs)
