from app.routers.decorators import request_decorator
from fastapi import APIRouter, Request

router = APIRouter()


@router.get('/account/sign-up')
@request_decorator
def sign_up_page(request: Request):
    return "sign_up.html", {}


@router.post('/account/sign-up')
@request_decorator
async def sign_up(request: Request):
    breakpoint()
    return "sign_up.html", {}


@router.get('/account/sign-in')
@request_decorator
def sign_up(request: Request):
    return "sign_in.html", {}


@router.post('/account/sign-in')
@request_decorator
async def sign_up(request: Request):
    return "sign_in.html", {}
