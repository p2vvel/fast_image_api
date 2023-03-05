from fastapi import FastAPI, Depends, UploadFile
from api import models, schemas, crud, database as db, config 
from sqlalchemy.orm import Session
import aiofiles     # asynchronous io
from pathlib import Path


app = FastAPI()
# migrate all tables (TODO: use alembic)
db.Base.metadata.create_all(bind=db.engine)


@app.get("/")
def root():
    return {
        "msg": "Hopefully, I'm gonna be pretty pretty API someday :)"
    }


@app.get("/images")
def get_images(db: Session = Depends(db.get_db)):
    images = crud.get_images(db)
    return images


@app.post("/images")
def upload_image(file: UploadFile, db: Session = Depends(db.get_db)):
    new_path = Path(config.FILE_STORAGE) / file.filename
    with open(new_path, "wb") as saved_file:
        content = file.file.read()
        saved_file.write(content)
    
    return file.headers