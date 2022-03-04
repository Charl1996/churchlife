from celery_service import celery_app


@celery_app.task
def send_wix_purchase_message_with_handler(handler, mobile_number, **kwargs):
    from app.messaging import MessagingService
    handler_class = MessagingService.get_handler_class(handler)
    handler_class.send_wix_purchase_message(mobile_number, **kwargs)
