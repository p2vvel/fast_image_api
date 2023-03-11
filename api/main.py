from fastapi import FastAPI, Depends, UploadFile
from api import models, schemas, crud, database as db, config 
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles




app = FastAPI()

app.mount("/static", StaticFiles(directory="./images"), name="static")
# migrate all tables (TODO: use alembic)
db.Base.metadata.create_all(bind=db.engine)


@app.get("/")
def root():
    return {
        "msg": "Hopefully, I'm gonna be pretty pretty API someday :)"
    }


@app.get("/images")
def get_images(db: Session = Depends(db.get_db)) -> list[schemas.OutputImage]:
    images = crud.get_images(db)
    return images


@app.post("/images")
def upload_image(file: UploadFile, db: Session = Depends(db.get_db)) -> schemas.OutputImage:
    created_image = crud.create_image(file, db)
    return created_image
