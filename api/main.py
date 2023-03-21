from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.images.main import router as image_router
from api.auth.main import router as auth_router

app = FastAPI()
# server static files
app.mount("/static", StaticFiles(directory="./images"), name="static")
app.mount("/auth", auth_router)


# make all migrations
from api.database import Base, engine
Base.metadata.create_all(bind=engine)





@app.get("/")
def foo():
    return "ASD"