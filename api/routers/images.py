from fastapi import Depends, UploadFile, APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..cruds import image as image_crud


router = APIRouter()


@router.get("/")
def get_images(db: Session = Depends(get_db)) -> list[schemas.OutputImage]:
    images = image_crud.get_images(db)
    return images


@router.post("/")
def upload_image(file: UploadFile, db: Session = Depends(get_db)) -> schemas.OutputImage:
    created_image = image_crud.create_image(file, db)
    return created_image
