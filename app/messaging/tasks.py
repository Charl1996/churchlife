from celery_service import celery_app


@celery_app.task
def send_wix_purchase_message_with_handler(handler, mobile_number, **kwargs):
    handler.send_wix_purchase_message(mobile_number, **kwargs)
