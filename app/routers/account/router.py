from app.routers.decorators import view_request
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get('/account/sign-up')
@view_request
def sign_up(request: Request):
    return "sign_up.html", {}


@router.post('/account/create')
async def create_account(request: Request):
    data = await request.json()
    # Create an organisation account
    return {"redirect_url": "/account/sign-in"}


@router.get('/account/sign-in')
@view_request
def sign_in(request: Request):
    return "sign_in.html", {}


@router.post('/account/sign-in')
async def sign_in(request: Request):
    data = await request.json()
    # Validate email and password
    # and return dashboard view with JWT or something
    return "sign_in.html", {}
