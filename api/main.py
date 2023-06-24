from fastapi import FastAPI
import os
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .routers import auth_router, images_router, users_router
from .config import settings
from contextlib import asynccontextmanager
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # check folder for serving static files
    if not os.path.exists(settings.file_storage):
        os.mkdir(settings.file_storage)

    # mount routers
    app.include_router(auth_router, prefix="/auth")
    app.include_router(users_router, prefix="/users")
    app.include_router(images_router, prefix=settings.image_url)

    # make all migrations
    Base.metadata.create_all(bind=engine)
    yield


tags_metadata = [
    {
        "name": "auth",
        "description": "Operations with users and authentication",
    },
    {
        "name": "images",
        "description": "Core API functionality",
    },
]


app = FastAPI(
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    title="Fast Image API",
    description="Simple API for uploading and editing images written in Python with FastAPI combined with Celery and SQLAlchemy",  # noqa: E501
    version=":)",
    contact={
        "name": "Paweł Śmiałek",
        "url": "https://github.com/p2vvel",
    },
)


@app.get("/", include_in_schema=False)
def root(db: Session = Depends(get_db)):
    return "Hello!"
