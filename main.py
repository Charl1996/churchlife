import uvicorn

from fastapi import FastAPI
from configs import (
    APPLICATION_HOST,
    APPLICATION_PORT,
)

from app.routers import account_router
from app.routers import webhooks_router
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Configure CORS
allowed_origins = [
    "http://127.0.0.1:8082",
    "http://localhost:8082",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(account_router)
app.include_router(webhooks_router)


def initialize_database():
    from postgresql import Base, engine
    Base.metadata.create_all(bind=engine)


@app.get('/')
def root():
    return RedirectResponse(url='/account/sign-in')


if __name__ == '__main__':
    initialize_database()

    uvicorn.run(
        'main:app',
        host=APPLICATION_HOST,
        port=APPLICATION_PORT,
        reload=True,
    )
