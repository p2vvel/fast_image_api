from fastapi import Depends, UploadFile, APIRouter, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..cruds import image as image_crud
from ..models import User
from ..dependencies.auth import get_user_or_401
from uuid import UUID, uuid4
from ..config import IMAGE_URL, FILE_STORAGE
from api.tasks.images import edit_image, app as celery_app
from celery.result import AsyncResult

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


@router.get("/status/{task_uuid}")
def get_edit_status(task_uuid: UUID):
    result = AsyncResult(str(task_uuid), app=celery_app)
    return {
        "status": result.status,
        "result": f"{result.result}" if result.status == "SUCCESS" else None
    }


# TODO: implement xsendfile - https://www.nginx.com/resources/wiki/start/topics/examples/xsendfile/
# temporary workaround for serving images below:
@router.get("/{user_uuid}/{image_uuid}")
def get_original_image(
    user_uuid: UUID,
    image_uuid: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_or_401),
) -> FileResponse:
    image = image_crud.get_image_by_uuid(image_uuid, db)
    if user_uuid != user.uuid or image.user != user:
        raise HTTPException(status_code=403)

    return FileResponse(image.path)


def get_edited_image(
    edit_uuid: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_or_401)
) -> FileResponse:
    pass


@router.get("/{user_uuid}/{image_uuid}/transform")
def send_edit_to_celery(
    user_uuid: UUID,
    image_uuid: UUID,
    transform: schemas.Transform,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_or_401),
):
    image = image_crud.get_image_by_uuid(image_uuid, db)
    if user_uuid != user.uuid or image.user != user:
        raise HTTPException(status_code=403)

    new_filename = f"{uuid4()}.png"
    task = edit_image.delay(image.path, new_filename, transform)

    return {
        "task_id": task.id,
        "status_url": f"{IMAGE_URL}/status/{task.id}"
    }
