from functools import wraps
from app.routers.helper import render_template
from fastapi.responses import RedirectResponse


def view_request(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        request = kwargs['request']

        response = view_function(*args, **kwargs)

        if type(response) == RedirectResponse:
            return response

        template = response.get('template')
        data = response.get('data', {})
        if template:
            return render_template(request, template, data)
        else:
            return response

    return wrapper
