from fastapi import APIRouter, Request
from app.messaging import MessagingService

router = APIRouter()


@router.post('/wix/purchase/', status_code=200)
def wix_purchase(request: Request):
    request_data = request.json()
    messaging_service = MessagingService()

    messaging_service.send_async_text_message(
        mobile_number=request_data.get('phone_number'),
        message='Thank you for this!',
        first_name=request_data.get('first_name'),
        last_name=request_data.get('last_name'),
    )
