from app.routers.decorators import view_request
from fastapi import Request, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse

from app.database.exceptions import DuplicateResourceError, ResourceNotFound
from app.organisations import Organisation
from app.users import User

from pydantic.error_wrappers import ValidationError
from app.routers.helper import get_current_user
from configs import JWT_COOKIE
from fastapi import APIRouter


router = APIRouter(
    dependencies=[],
)


@router.get('/account/create')
@view_request
def create_account(request: Request):
    return {'template': "create_account.html"}


@router.post('/account/create')
async def create_account(request: Request):
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

    try:
        organisation = Organisation.create(data=data['organisation'])
    except ValidationError as _error:
        raise HTTPException(status_code=422, detail='Missing organisation data')
    except DuplicateResourceError:
        User.delete(user_id=user.fields.id)
        raise HTTPException(
            status_code=422,
            detail='Domain already exists!'
        )
    organisation.add_user(user)

    return JSONResponse(status_code=200)


@router.get('/account/sign-in')
@view_request
def sign_in(request: Request):
    return {'template': "sign_in.html"}


@router.post('/account/sign-in')
async def sign_in(request: Request):
    data = await request.json()

    try:
        jwt = User.log_in(data['email'], data['password'])
    except ResourceNotFound:
        jwt = None

    if jwt is None:
        raise HTTPException(status_code=403, detail='Invalid credentials')

    response = JSONResponse(status_code=200)
    response.set_cookie(key=JWT_COOKIE, value=jwt)
    return response


@router.post('/account/sign-out')
def sign_out(request: Request):
    response = JSONResponse(status_code=200)
    response.set_cookie(key=JWT_COOKIE, value=None)
    return response


@router.get('/account/user')
@view_request
def user_profile(request: Request, user: User = Depends(get_current_user)):
    return {
        'template': "user_profile.html",
        'data': {
            'user': {
                'first_name': user.fields.first_name,
                'last_name': user.fields.last_name,
                'email': user.fields.email,
            },
        }
    }


@router.get('/account/organisations')
@view_request
def show_organisations(request: Request, user: User = Depends(get_current_user)):
    organisations = user.organisations

    if len(organisations) == 1:
        org = organisations[0]
        return RedirectResponse(url='/{domain}/dashboard'.format(domain=org.domain))

    return {
        'template': "organisations.html",
        'data': {
            'organisations': organisations,
        }
    }
