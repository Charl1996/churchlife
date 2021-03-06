import json

from app.routers.decorators import view_request, domain_request
from fastapi import Request, Depends
from fastapi_cache.backends.redis import RedisCacheBackend
from app.organisations import Organisation
from app.users import User
from app.routers.helper import get_current_user
from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from pydantic.error_wrappers import ValidationError
from app.database.exceptions import DuplicateResourceError
from app.integrations.utils import test_database_platform_connection, test_messaging_platform_connection
from app.integrations.database.database_platform import DatabasePlatform
from app.integrations.messaging.messaging_platform import MessagingPlatform
from app.notifications import Notification
from app.workflows.triggers.trigger import TrackingEventTrigger
from app.events import Event, TrackingEvent, SessionEvent
from app.workflows.actions.action import Action
from app.cache import redis_cache, DATABASE_ENTITIES_CACHE_KEY


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


@router.post('/{domain}/events/calendar-data')
@domain_request
async def get_calendar_data(request: Request, domain: str, user: User = Depends(get_current_user)):
    post_data = await request.json()
    org = Organisation.get_by_domain(domain)

    data = []
    for event in org.get_event_sessions_in_time_interval(
        start=post_data['start'],
        end=post_data['end'],
    ):
        event_dict = event.dict()
        event_dict['date'] = str(event_dict['date'])  # There should be better way to do this
        data.append(event_dict)

    return JSONResponse(status_code=200, content=data)


@router.get('/{domain}/events/new')
@view_request
@domain_request
async def new_event(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain)

    data = {
        'notifications': org.get_notifications(),
        'trigger_types': TrackingEventTrigger.SUPPORTED_TYPES,
    }

    return {'template': 'layout_content/events/new.html', 'data': data}


@router.post('/{domain}/events/new')
@domain_request
async def create_event(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()

    try:
        organisation = Organisation.get_by_domain(domain=domain)
        data['event']['organisation_id'] = organisation.fields.id

        organisation.create_event(
            event_detail=data['event'],
            attendance_tracking_detail=data['attendance_tracking'],
        )
    except ValidationError as _error:
        raise HTTPException(status_code=422, detail='Missing some data')

    return JSONResponse(status_code=200)


@router.delete('/{domain}/events/{event_id}')
@domain_request
async def delete_event_by_(request: Request, domain: str, event_id: int, user: User = Depends(get_current_user)):
    tracking_event = TrackingEvent.get_by(criteria={'event_id': event_id})

    tracking_event_triggers = TrackingEventTrigger.get_all_by(criteria={'tracking_event_id': tracking_event.id})
    for tet in tracking_event_triggers:
        actions = Action.get_all_by(criteria={'tracking_event_trigger_id': tet.id})
        for action in actions:
            Action.delete(action.id)
        TrackingEventTrigger.delete(tet.id)

    TrackingEvent.delete(tracking_event.id)
    Event.delete(event_id)

    return JSONResponse(status_code=200)


@router.get('/{domain}/events/sessions/{session_event_id}')
@view_request
@domain_request
async def view_session_event(request: Request, domain: str, session_event_id: int, user: User = Depends(get_current_user)):
    session_event = SessionEvent.get(session_event_id)
    data = session_event.event_details().dict()

    return {'template': 'layout_content/events/view_session.html', 'data': data}


@router.post('/{domain}/events/sessions/{session_event_id}/cancel')
@domain_request
async def cancel_session_event(request: Request, domain: str, session_event_id: int, user: User = Depends(get_current_user)):

    return JSONResponse(status_code=200)


@router.get('/{domain}/notifications')
@view_request
@domain_request
async def notifications(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain)
    notifications_schemas = org.get_notifications()

    notifications_data = []
    for notification in notifications_schemas:
        notifications_data.append(notification)

    data = {
        'notifications': notifications_data
    }

    return {'template': 'layout_content/notifications/list.html', 'data': data}


@router.get('/{domain}/notifications/new')
@view_request
@domain_request
async def new_notification(request: Request, domain: str, user: User = Depends(get_current_user)):
    return {'template': 'layout_content/notifications/new.html'}


@router.post('/{domain}/notifications/new')
@domain_request
async def new_notification(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()
    org = Organisation.get_by_domain(domain)

    try:
        # Todo: do inside transaction
        notification = Notification.create(data={
            'name': data['name'],
            'organisation_id': org.fields.id,
        })
        for notification_item in data['notification_members']:
            notification.add_notification_item(
                item_type=notification_item['type'],
                data=notification_item['data'],
            )

    except Exception as e:
        return HTTPException(status_code=422, detail='Could not create notifications')

    return JSONResponse(status_code=200)


@router.delete('/{domain}/notifications/{notification_id}')
@domain_request
async def delete_notification(request: Request, domain: str, notification_id: str, user: User = Depends(get_current_user)):
    Notification.delete(model_id=notification_id)
    return JSONResponse(status_code=200)


@router.get('/{domain}/settings')
@view_request
@domain_request
async def settings(request: Request, domain: str, user: User = Depends(get_current_user)):
    org = Organisation.get_by_domain(domain)
    return {'template': 'layout_content/settings.html', 'data': org.updateable_details.dict()}


@router.post('/{domain}/settings')
@domain_request
async def settings(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()

    org = Organisation.get_by_domain(domain)
    org.update_details(data)

    return JSONResponse(status_code=200)


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

    return {'template': 'layout_content/users/new.html', 'data': data}


@router.post('/{domain}/users/new')
@domain_request
async def invite_new_user(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()

    try:
        user = User.get_by_email(data['user']['email'])

        if not user:
            user = User.create(data=data['user'])
    except ValidationError as _error:
        raise HTTPException(status_code=422, detail='Missing user data')
    except DuplicateResourceError:
        raise HTTPException(
            status_code=422,
            detail='Email already exists!'
        )

    organisation = Organisation.get_by_domain(domain)

    if not user.get_user_organisation_by_domain(domain):
        organisation.invite_new_user(user)

    return JSONResponse(status_code=200)


@router.delete('/{domain}/users/{user_id}')
@domain_request
async def delete_organisation_user(request: Request, domain: str, user_id: str, user: User = Depends(get_current_user)):
    organisation = Organisation.get_by_domain(domain)
    organisation.remove_user(user_id=user_id)
    return JSONResponse(status_code=200)


@router.get('/{domain}/users/{user_id}/edit')
@view_request
@domain_request
async def get_new_user(request: Request, domain: str, user_id: str, user: User = Depends(get_current_user)):
    from app.organisations.organisation_schema import OrganisationUserViewSchema

    user = User.get_by_id(user_id)
    if not user:
        JSONResponse(status_code=404)

    data = OrganisationUserViewSchema(
        id=user.fields.id,
        first_name=user.fields.first_name,
        last_name=user.fields.last_name,
        email=user.fields.email,
    ).dict()

    return {'template': 'layout_content/users/edit_user.html', 'data': data}


@router.get('/{domain}/database')
@view_request
@domain_request
async def get_database_platform(request: Request, domain: str, user: User = Depends(get_current_user)):
    organisation = Organisation.get_by_domain(domain)
    platform = organisation.get_linked_database_platform()

    data = {'database': None, 'entities': []}
    if platform:
        data['database'] = platform.fields.dict()
        # data['entities'] = platform.get_entities(as_dict=True)

    return {'template': 'layout_content/database/database.html', 'data': data}


@router.get('/{domain}/database/entities')
@view_request
@domain_request
async def get_database_platform(
        request: Request,
        domain: str,
        user: User = Depends(get_current_user),
        cache: RedisCacheBackend = Depends(redis_cache),
):
    # entities = await cache.get(DATABASE_ENTITIES_CACHE_KEY, [])
    # if not entities:
    organisation = Organisation.get_by_domain(domain)
    platform = organisation.get_linked_database_platform()

    data = {'database': None, 'entities': []}
    if platform:
        data['entities'] = platform.get_entities(as_dict=True)
            # await cache.set(DATABASE_ENTITIES_CACHE_KEY, entities)

    return {'template': 'layout_content/database/database_entities_list.html', 'data': data}


@router.post('/{domain}/database/test-connection')
@domain_request
async def test_connection(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()
    status_code, errors = test_database_platform_connection(data['platform'], data["configuration"])

    if status_code not in [200, 403]:
        return JSONResponse(status_code=422, content=errors)
    else:
        return JSONResponse(status_code=status_code, content=errors)


@router.post('/{domain}/database/new')
@domain_request
async def create_new_database_platform(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()
    organisation = Organisation.get_by_domain(domain)

    try:
        data['configuration']['organisation_id'] = organisation.fields.id

        if DatabasePlatform.linked_to_organisation(
                organisation_id=organisation.fields.id,
                slug=data['platform'],
                api_key=data['configuration']['api_key']):
            raise DuplicateResourceError

        _platform = DatabasePlatform.create_platform(data['platform'], data['configuration'])
    except ValidationError as _error:
        raise HTTPException(status_code=422, detail='Missing some data')
    except DuplicateResourceError:
        raise HTTPException(
            status_code=422,
            detail=f"Platform with provided API key already linked"
        )

    return JSONResponse(status_code=200)


@router.get('/{domain}/messaging')
@view_request
@domain_request
async def messaging(request: Request, domain: str, user: User = Depends(get_current_user)):
    organisation = Organisation.get_by_domain(domain)
    platform = organisation.get_linked_messaging_platform()

    data = {}
    if platform:
        data = platform.dict()

    return {'template': 'layout_content/messaging.html', 'data': data}


@router.post('/{domain}/messaging/test-connection')
@domain_request
async def test_messaging_connection(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()
    status_code, errors = test_messaging_platform_connection(data['platform'], data["configuration"])

    if status_code not in [200, 403]:
        return JSONResponse(status_code=422, content=errors)
    else:
        return JSONResponse(status_code=status_code, content=errors)


@router.post('/{domain}/messaging/new')
@domain_request
async def new_messaging_platform(request: Request, domain: str, user: User = Depends(get_current_user)):
    data = await request.json()
    organisation = Organisation.get_by_domain(domain)

    try:
        data['configuration']['organisation_id'] = organisation.fields.id
        if MessagingPlatform.linked_to_organisation(
                organisation_id=organisation.fields.id,
                slug=data['platform'],
                api_key=data['configuration']['api_key']):
            raise DuplicateResourceError

        _platform = MessagingPlatform.create_platform(data['platform'], data['configuration'])
    except ValidationError as _error:
        raise HTTPException(status_code=422, detail='Missing some data')
    except DuplicateResourceError:
        raise HTTPException(
            status_code=422,
            detail=f"Platform with provided API key already linked"
        )

    return JSONResponse(status_code=200)
