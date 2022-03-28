from app.routers.decorators import view_request, domain_request
from fastapi import Request, Depends
from app.organisations import Organisation
from app.users import User
from app.routers.helper import get_current_user
from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from pydantic.error_wrappers import ValidationError

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
    # Add some kind of dashboard?
    # return dashboard view

    # For now, redirect to events page
    return RedirectResponse(url=f'/{domain}/events')


@router.get('/{domain}/events')
@view_request
@domain_request
def events(request: Request, domain: str, user: User = Depends(get_current_user)):
    return {'template': 'layout_content/events/list.html'}


@router.get('/{domain}/events/new')
@view_request
@domain_request
def events(request: Request, domain: str, user: User = Depends(get_current_user)):
    return {'template': 'layout_content/events/new_event.html'}


@router.get('/{domain}/events/{event_id}')
@view_request
@domain_request
def get_event(request: Request, domain: str, event_id: int, user: User = Depends(get_current_user)):
    return {'template': 'layout_content/events/show_event.html'}


@router.post('/{domain}/event')
@domain_request
async def create_event(request: Request, domain: str, user: User = Depends(get_current_user)):
    from app.events import Event
    data = await request.json()
    breakpoint()
    try:
        event = Event.create(data=data['event'])
    except ValidationError as _error:
        raise HTTPException(status_code=422, detail='Missing user data')

    # Need to create the ScheduleTrigger and action also

    return None  # Redirect to events view


@router.get('/{domain}/tracking')
@view_request
@domain_request
def tracking(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/tracking.html', 'data': data}


@router.get('/{domain}/settings')
@view_request
@domain_request
def settings(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/settings.html', 'data': data}


@router.get('/{domain}/users')
@view_request
@domain_request
def users(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/users.html', 'data': data}


@router.get('/{domain}/database')
@view_request
@domain_request
def database(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/database.html', 'data': data}


@router.get('/{domain}/messaging')
@view_request
@domain_request
def messaging(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/messaging.html', 'data': data}
