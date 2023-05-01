from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi import Depends
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .routers import auth_router, images_router, users_router


app = FastAPI()

# serve static files
if not os.path.exists("./images"):
    os.mkdir("./images")

app.mount("/static", StaticFiles(directory="./images"), name="static")
app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/users")
app.include_router(images_router, prefix="/images")


# make all migrations
Base.metadata.create_all(bind=engine)


@app.get("/")
def root(db: Session = Depends(get_db)):
    return "Hello!"
