from app.integrations.database_service.handlers.breeze import Breeze
from configs import DEFAULT_DATABASE_HANDLER

HANDLERS = {
    'breeze': Breeze
}


class DatabaseManagementService:
    """
    This is the 'public' facing class that should be used to interface with
    the database management system.
    """
    handler_slug: str

    def __init__(self, handler=DEFAULT_DATABASE_HANDLER):
        self.handler_slug = handler

    @classmethod
    def get_handler_class(cls, handler_slug):
        return HANDLERS[handler_slug]()

    def get_people(self):
        return self.get_handler_class(self.handler_slug).get_people()

    def update_person(self):
        pass
