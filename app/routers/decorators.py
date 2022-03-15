from functools import wraps
from app.routers.helper import render_template
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException


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


def domain_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        domain = kwargs.get('domain')
        user = kwargs.get('user')

        if not user.belongs_to_domain(domain):
            raise HTTPException(status_code=403, detail='User does not have access to domain')

        return func(*args, **kwargs)
    return wrapper
