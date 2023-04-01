from .database import Base, engine
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import auth_router, image_router


app = FastAPI()
# server static files
app.mount("/static", StaticFiles(directory="./images"), name="static")
app.mount("/auth", auth_router)
app.mount("/images", image_router)


# make all migrations
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return "Hello!"
