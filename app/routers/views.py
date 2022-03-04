from app.routers.decorators import request_decorator
from fastapi import APIRouter, Request

router = APIRouter()


@router.get('/')
@request_decorator
def home(request: Request):
    return "home.html", {}
