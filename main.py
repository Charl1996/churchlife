import uvicorn
from fastapi import FastAPI

from configs import (
    APPLICATION_HOST,
    APPLICATION_PORT,
)
from app.messenger import MessengerService

app = FastAPI()


@app.post('/wix/incoming')
def wix_incoming(data):
    mobile_number = data.get('mobile_number')

    service = MessengerService()
    service.send_message(
        mobile_number=mobile_number,
        message='Thank you for this!',
    )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=APPLICATION_HOST,
        port=APPLICATION_PORT,
        reload=True,
    )
