from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from .database import Base, engine
from .routers import auth_router, image_router


app = FastAPI()
# server static files

if not os.path.exists("./images"):
    os.mkdir("./images")

app.mount("/static", StaticFiles(directory="./images"), name="static")
app.mount("/auth", auth_router)
app.mount("/images", image_router)


# make all migrations
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return "Hello!"
