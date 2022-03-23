from app.routers.decorators import view_request, domain_request
from fastapi import Request, Depends
from app.organisations import Organisation
from app.users import User
from app.routers.helper import get_current_user
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.routers.helper import render_template
from fastapi_sqlalchemy import db


router = APIRouter()


@router.post('/{domain}/upload-logo')
# @domain_request
async def dashboard(request: Request, domain: str):
    data = await request.form()
    image_file = data['file']
    image_bytes = await image_file.read()

    organisation = Organisation.get_by_domain(domain=domain)
    organisation.set_logo(image_bytes)

    return JSONResponse(status_code=200)


@router.get('/{domain}/dashboard')
@view_request
@domain_request
def dashboard(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain=domain)
    # And some other stuff...
    return {
        'template': "layout.html",
        'data': {
            'organisation': {
                'name': org.fields.name,
            },
            'initial_page': 'summary.html',
        }
    }


"""
The following "views" works by returning rendered content which is simply
used to replace a certain <div> element using jQuery. 
"""


@router.get('/{domain}/summary')
@domain_request
def summary(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain=domain)

    data = {}

    return render_template(request, 'layout_content/summary.html', data)


@router.get('/{domain}/events')
@domain_request
def events(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain=domain)

    data = {}

    return render_template(request, 'layout_content/events.html', data)


@router.get('/{domain}/tracking')
@domain_request
def tracking(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain=domain)

    data = {}

    return render_template(request, 'layout_content/tracking.html', data)


@router.get('/{domain}/settings')
@domain_request
def settings(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain=domain)

    data = {}

    return render_template(request, 'layout_content/settings.html', data)


@router.get('/{domain}/users')
@domain_request
def users(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain=domain)

    data = {}

    return render_template(request, 'layout_content/users.html', data)


@router.get('/{domain}/database')
@domain_request
def database(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain=domain)

    data = {}

    return render_template(request, 'layout_content/database.html', data)


@router.get('/{domain}/messaging')
@domain_request
def messaging(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain=domain)

    data = {}

    return render_template(request, 'layout_content/messaging.html', data)
