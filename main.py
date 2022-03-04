import uvicorn

from fastapi import FastAPI
from configs import (
    APPLICATION_HOST,
    APPLICATION_PORT,
)

from app.routers import views_router
from app.routers import webhooks_router

app = FastAPI()

# Configure application
app.include_router(views_router)
app.include_router(webhooks_router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=APPLICATION_HOST,
        port=APPLICATION_PORT,
        reload=True,
    )
