from fastapi import APIRouter, Request
from app.messaging import MessagingService

router = APIRouter()


# This route and logic will need to conform to the trigger-action
# logic in the future
@router.post('/wix/purchase/', status_code=200)
def wix_purchase(request: Request):
    breakpoint()

    request_data = request.json()
    messaging_service = MessagingService()

    messaging_service.send_wix_purchase_message(
        mobile_number=request_data.get('phone_number'),
        first_name=request_data.get('first_name'),
        last_name=request_data.get('last_name'),
    )
