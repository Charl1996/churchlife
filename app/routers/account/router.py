from app.routers.decorators import view_request
from fastapi import APIRouter, Request

router = APIRouter()


@router.get('/account/create')
@view_request
def create_account(request: Request):
    return "create_account.html", {}


@router.post('/account/create')
async def create_account(request: Request):
    data = await request.json()
    # Create an organisation account
    return {"redirect_url": "/account/create"}


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
