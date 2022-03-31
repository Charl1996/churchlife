from functools import wraps
from app.routers.helper import render_template
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from app.users import UserOrganisationView, UserView
from pydantic import parse_obj_as


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

        organisation = user.get_user_organisation_by_domain(domain)
        if organisation is None:
            raise HTTPException(status_code=403, detail='User does not have access to domain')

        response = func(*args, **kwargs)

        if type(response) == RedirectResponse:
            return response

        # Inject the organisation in response
        data = response.get('data', {})
        data['organisation'] = parse_obj_as(UserOrganisationView, organisation.fields)
        # data['user'] = parse_obj_as(UserView, user.fields)
        return {'data': data, **response}

    return wrapper
