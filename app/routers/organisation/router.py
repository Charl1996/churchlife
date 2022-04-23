from app.routers.decorators import view_request, domain_request
from fastapi import Request, Depends
from app.organisations import Organisation
from app.users import User
from app.routers.helper import get_current_user
from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from pydantic.error_wrappers import ValidationError
from app.database.exceptions import DuplicateResourceError

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
async def dashboard(request: Request, domain: str, user: User = Depends(get_current_user)):
    # Add some kind of dashboard?
    # return dashboard view

    # For now, redirect to events page
    return RedirectResponse(url=f'/{domain}/events')


@router.get('/{domain}/events')
@view_request
@domain_request
async def events(request: Request, domain: str, user: User = Depends(get_current_user)):
    return {'template': 'layout_content/events/list.html'}


@router.get('/{domain}/events/new')
@view_request
@domain_request
async def events(request: Request, domain: str, user: User = Depends(get_current_user)):
    return {'template': 'layout_content/events/new_event.html'}


@router.post('/{domain}/events/new')
@domain_request
async def create_event(request: Request, domain: str, user: User = Depends(get_current_user)):
    breakpoint()
    data = await request.json()
    breakpoint()

    # example_data = {
    #     'event': {
    #         'name': '<name>',
    #         'type': 'one-time' / 'series',
    #         'interval': 'daily' / 'weekly' / 'monthly',
    #         'from_date': '<date>',
    #         'to_date': '<date>' / '',
    #         'start_at': '<time>',
    #         'end_at': '<time>'m
    #     },
    #     'attendance_tracker': {
    #         'start_before': '',
    #         'stop_after': '',
    #     }
    # }

    try:
        organisation = Organisation.get_by_domain(domain=domain)
        organisation_event = organisation.create_event(data=data['event'])
    except ValidationError as _error:
        raise HTTPException(status_code=422, detail='Missing some data')

    if data.get('attendance_tracker'):
        try:
            organisation_event = organisation_event.add_attendance_tracker(data=data['attendance_tracker'])
        except ValidationError as _error:
            raise HTTPException(status_code=422, detail='Missing some data')
        # Need to create the ScheduleTrigger and action also

    return None  # Redirect to events view


@router.get('/{domain}/events/{event_id}')
@view_request
@domain_request
async def get_event(request: Request, domain: str, event_id: int, user: User = Depends(get_current_user)):
    return {'template': 'layout_content/events/show_event.html'}


@router.get('/{domain}/tracking')
@view_request
@domain_request
async def tracking(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/tracking.html', 'data': data}


@router.get('/{domain}/settings')
@view_request
@domain_request
async def settings(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/settings.html', 'data': data}


@router.get('/{domain}/users')
@view_request
@domain_request
async def users(request: Request, domain: str, user: User = Depends(get_current_user)):
    organisation = Organisation.get_by_domain(domain)
    data = {
        'users': organisation.get_users()
    }

    return {'template': 'layout_content/users/list.html', 'data': data}


@router.get('/{domain}/users/new')
@view_request
@domain_request
async def get_new_user(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/users/new_user.html', 'data': data}


@router.post('/{domain}/users/new')
@domain_request
async def invite_new_user(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()

    try:
        user = User.create(data=data['user'])
    except ValidationError as _error:
        raise HTTPException(status_code=422, detail='Missing user data')
    except DuplicateResourceError:
        raise HTTPException(
            status_code=422,
            detail='Email already exists!'
        )

    organisation = Organisation.get_by_domain(domain)
    organisation.invite_new_user(user)
    return JSONResponse(status_code=200)


@router.delete('/{domain}/users/{user_id}')
@domain_request
async def delete_organisation_user(request: Request, domain: str, user_id: str, user: User = Depends(get_current_user)):
    organisation = Organisation.get_by_domain(domain)
    organisation.remove_user(user_id=user_id)
    return JSONResponse(status_code=200)


@router.get('/{domain}/database')
@view_request
@domain_request
async def database(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/database.html', 'data': data}


@router.get('/{domain}/messaging')
@view_request
@domain_request
async def messaging(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = {}

    return {'template': 'layout_content/messaging.html', 'data': data}
