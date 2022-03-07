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


@app.get('/')
def root():
    return RedirectResponse(url='/account/sign-in')


def configure_cors(application):
    allowed_origins = [
        "http://127.0.0.1:8082",
        "http://localhost:8082",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_application_static_files(application):
    application.mount("/static", StaticFiles(directory="static"), name="static")


def configure_application_routers(application):
    application.include_router(account_router)
    application.include_router(webhooks_router)


def init_db():
    from postgresql import Base, engine
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    configure_application_routers(app)
    init_db()

    uvicorn.run(
        'main:app',
        host=APPLICATION_HOST,
        port=APPLICATION_PORT,
        reload=True,
    )
