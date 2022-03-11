from app.routers.decorators import view_request
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from postgresql import DBSession
from app.database.exceptions import DuplicateResourceError
from app.organisations import Organisation
from app.users import User

from pydantic.error_wrappers import ValidationError

router = APIRouter()


@router.get('/account/create')
@view_request
def create_account(request: Request):
    return "create_account.html", {}


@router.post('/account/create')
async def create_account(request: Request):
    data = await request.json()
    with DBSession() as db_session:
        try:
            user = User.create(db_session=db_session, data=data['user'])
        except ValidationError as _error:
            return HTTPException(status_code=422, detail='Missing user data')
        except DuplicateResourceError:
            return HTTPException(
                status_code=422,
                detail='Duplicate resource detected! The email probably already exists!'
            )

        try:
            organisation = Organisation.create(db_session=db_session, data=data['organisation'])
        except ValidationError as _error:
            return HTTPException(status_code=422, detail='Missing organisation data')
        except DuplicateResourceError:
            # Need to implement
            User.delete(db_session=db_session, user_id=user.fields.id)

            return HTTPException(
                status_code=422,
                detail='Duplicate resource detected! The domain probably already exists!'
            )

        organisation.add_user(user)

    return JSONResponse(status_code=200, content={"redirect_url": "/account/sign-in"})


@router.get('/account/sign-in')
@view_request
def sign_in(request: Request):
    return "sign_in.html", {}


@router.post('/account/sign-in')
async def sign_in(request: Request):
    data = await request.json()
    # Validate email and password
    # and return dashboard view with session token or something
    return "sign_in.html", {}


@router.get('/domain')
@view_request
def dashboard(request: Request):
    return "/layout_content/dashboard.html", {
        'organisation': 'Gesinskerk',
    }

#
# @router.get('/{domain}/dashboard')
# def dashboard(request: Request):
#     return "dashboard.html", {}
