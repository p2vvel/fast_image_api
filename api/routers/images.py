from fastapi import Depends, UploadFile, APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..cruds import image as image_crud
from ..models import User
from ..dependencies.auth import get_user_or_401
from uuid import UUID


router = APIRouter()


@router.post("/")
def upload_image(
    file: UploadFile, db: Session = Depends(get_db), user: User = Depends(get_user_or_401)
) -> schemas.OutputImage:
    created_image = image_crud.create_image(file, user, db)
    return created_image


@router.get("/")
def get_images(
    db: Session = Depends(get_db), user: User = Depends(get_user_or_401)
) -> list[schemas.OutputImage]:
    images = image_crud.get_images(db)
    return images


@router.get("/{user_uuid}/{image_uuid}")
def get_original_image(
    user_uuid: UUID,
    image_uuid: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_or_401),
):
    # image = image_crud.get_original_image(user_id, image_id, db)
    # return image 
    print("USER UUID: ", user_uuid)
    print("IMAGE UUID: ", image_uuid)
    pass
    return "HI"


@router.get("/{user_uuid}/{image_uuid}/transform")
def edit_image(
    user_uuid: UUID,
    image_uuid: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_or_401),
):
    # image = image_crud.get_original_image(user_id, image_id, db)
    # return image
    print("USER UUID: ", user_uuid)
    print("IMAGE UUID: ", image_uuid)
    pass
    return "HI"
