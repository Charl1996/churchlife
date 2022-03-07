from fastapi import APIRouter, Request
from app.messaging import MessagingService
from logger import logger

router = APIRouter()


# This route and logic will need to conform to the trigger-action
# logic in the future
# @router.post('/wix/purchase/', status_code=200)
# async def wix_purchase(request: Request):
#     request_data = await request.json()
#     logger.info(f"Webhook received 'wix_purchase' : data => {request_data}")
#
#     messaging_service = MessagingService()
#     messaging_service.send_wix_purchase_message(
#         mobile_number=request_data.get('phone_number'),
#         first_name=request_data.get('first_name'),
#         last_name=request_data.get('last_name'),
#     )

@router.post('{domain}/webhook/incoming/', status_code=200)
async def webhook_trigger(request: Request):
    request_data = await request.json()
    pass
