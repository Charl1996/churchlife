from app.routers.decorators import view_request
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from postgresql import get_db
from app.database.exceptions import DuplicateResourceError
from app.organisations import OrganisationHandler as Organisation
from app.organisations.organisation_schema import OrganisationCreate
from app.users import UserHandler as User
from app.users.user_schema import UserCreate

from pydantic.error_wrappers import ValidationError

router = APIRouter()


@router.get('/account/create')
@view_request
def create_account(request: Request):
    return "create_account.html", {}


@router.post('/account/create')
async def create_account(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    try:
        user_data = UserCreate(**data['user'])
        user = User.create(db=db, user=user_data)
    except ValidationError as _error:
        return HTTPException(status_code=422, detail='Missing user data')
    except DuplicateResourceError:
        return HTTPException(
            status_code=422,
            detail='Duplicate resource detected! The email probably already exists!'
        )

    try:
        org_data = OrganisationCreate(**data['organisation'])
        org = Organisation.create(db=db, organisation=org_data)
    except ValidationError as _error:
        return HTTPException(status_code=422, detail='Missing organisation data')
    except DuplicateResourceError:
        # Need to implement
        User.delete(user.id)

        return HTTPException(
            status_code=422,
            detail='Duplicate resource detected! The domain probably already exists!'
        )

    Organisation.add_user_to_organisation(
        db=db,
        user=user,
        organisation=org,
    )

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
