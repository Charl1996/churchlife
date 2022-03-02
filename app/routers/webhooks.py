from fastapi import APIRouter, Request
from app.messaging import MessagingService

router = APIRouter()


@router.post('/wix/purchase', status_code=200)
def wix_purchase(request: Request):
    request_data = request.json()
    mobile_number = request_data.get('')

    service = MessagingService()
    service.send_async_text_message(
        mobile_number=mobile_number,
        message='Thank you for this!',
    )

    return
