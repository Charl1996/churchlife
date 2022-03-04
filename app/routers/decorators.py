from functools import wraps
from fastapi.templating import Jinja2Templates

# Configure templates
view_templates = Jinja2Templates(directory="app/templates")


def request_decorator(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        request = kwargs['request']
        template, data = view_function(*args, **kwargs)

        return view_templates.TemplateResponse(
            template,
            context={
                'request': request,
                'organization_name': 'Gesinskerk',
                **data,
            }
        )
    return wrapper
