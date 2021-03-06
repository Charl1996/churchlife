import uvicorn

from configs import (
    APPLICATION_HOST,
    APPLICATION_PORT,
    SQLALCHEMY_DATABASE_URL,
)

from app.routers import (
    account_router,
    organisation_router,
)

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi import FastAPI

from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend


app = FastAPI()

# Configure CORS
allowed_origins = [
    "http://127.0.0.1:8082",
    "http://localhost:8082",
]

app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(account_router)
app.include_router(organisation_router)


@app.get('/')
def root():
    return RedirectResponse(url='/account/sign-in')


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend('redis://redis')
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=APPLICATION_HOST,
        port=APPLICATION_PORT,
        reload=True,
    )
