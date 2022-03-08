from app.routers.decorators import view_request
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from postgresql import get_db
from app.organisations import OrganisationCreate, create_organisation
from app.users import UserCreate, create_user


router = APIRouter()


@router.get('/account/create')
@view_request
def create_account(request: Request):
    return "create_account.html", {}


@router.post('/account/create')
async def create_account(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    org_model = OrganisationCreate(
        name=data['organisation']['name'],
        domain=data['organisation']['domain']
    )
    org = create_organisation(db=db, organisation=org_model)

    user = UserCreate(
        first_name=data['user']['first_name'],
        last_name=data['user']['last_name'],
        email=data['user']['email'],
        password=data['user']['password'],
        organisation_id=org.id,
    )

    user = create_user(db=db, user=user)
    # send email

    return {"redirect_url": "/account/sign-in"}


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
