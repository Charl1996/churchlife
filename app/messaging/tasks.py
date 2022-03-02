from celery_service import celery_app


@celery_app.task
def send_text_message_with_handler(handler, mobile_number, message):
    handler.send_message(mobile_number, message)
