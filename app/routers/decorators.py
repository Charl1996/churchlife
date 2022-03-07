from functools import wraps
from fastapi.templating import Jinja2Templates

# Configure templates
view_templates = Jinja2Templates(directory="templates")


def view_request(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        request = kwargs['request']
        template, data = view_function(*args, **kwargs)

        return view_templates.TemplateResponse(
            template,
            context={
                'request': request,
                **data,
            },
        )
    return wrapper


def session_request(view_function):
    @wraps
    def wrapper(*args, **kwargs):
        # Get the session token and check if user is logged in
        return True
    return wrapper