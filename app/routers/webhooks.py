from fastapi import APIRouter, Request
from app.messenger import MessengerService

router = APIRouter()


@router.post('/wix/purchase', status_code=200)
def wix_purchase(request: Request):
    request_data = request.json()
    mobile_number = request_data.get('')

    service = MessengerService()
    service.send_message(
        mobile_number=mobile_number,
        message='Thank you for this!',
    )

    return
