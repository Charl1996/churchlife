import uvicorn
from fastapi import FastAPI
from configs import (
    APPLICATION_HOST,
    APPLICATION_PORT,
)
from app.routers import webhook_router


app = FastAPI()
app.include_router(webhook_router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=APPLICATION_HOST,
        port=APPLICATION_PORT,
        reload=True,
    )
