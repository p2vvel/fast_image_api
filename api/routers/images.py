from fastapi import Depends, UploadFile, APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..cruds import image as image_crud
from ..models import User
from ..dependencies.auth import get_user_or_401
from uuid import UUID, uuid4
from api.tasks.images import edit_image
from pathlib import Path
from ..config import settings
from ..utils.images import get_image_file


router = APIRouter()


@router.post(
    "/",
    tags=["images"],
    status_code=status.HTTP_201_CREATED,
    response_description="Created image metadata",
)
def upload_image(
    file: UploadFile, db: Session = Depends(get_db), user: User = Depends(get_user_or_401)
) -> schemas.OutputImage:
    """Upload new image"""
    created_image = image_crud.create_image(file, user, db)
    return created_image


# TODO: permissions!
@router.get("/", tags=["images"], response_description="List of images")
def get_images(
    db: Session = Depends(get_db), user: User = Depends(get_user_or_401)
) -> list[schemas.OutputImage]:
    images = image_crud.get_images(db)
    return images


@router.get("/status/{task_uuid}", tags=["images"], response_description="Edit task status")
def get_edit_status(
    task_uuid: UUID, db: Session = Depends(get_db), user: User = Depends(get_user_or_401)
):
    task_celery = image_crud.get_celery_task(task_uuid)
    task_db = image_crud.get_edit_task(task_uuid, db)
    if task_db.image.user != user:
        raise HTTPException(status_code=403)

    return {
        "status": task_celery.status,
        "result": f"{task_celery.result}" if task_celery.status == "SUCCESS" else None,
        "file": f"/edited/{task_uuid}",
    }


@router.get("/edited/{edit_uuid}", tags=["images"], response_description="Edited image file")
def get_edited_image(
    edit_uuid: UUID, db: Session = Depends(get_db), user: User = Depends(get_user_or_401)
) -> FileResponse:
    edit_task = image_crud.get_edit_task(edit_uuid, db)
    image = edit_task.image
    if image.user != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    result = image_crud.get_celery_task(edit_uuid)
    return get_image_file(result.result)


@router.get(
    "/{user_uuid}/{image_uuid}", tags=["images"], response_description="Uploaded image file"
)
def get_original_image(
    user_uuid: UUID,
    image_uuid: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_or_401),
) -> FileResponse:
    """Fetch previously uploaded image"""
    image = image_crud.get_image_by_uuid(image_uuid, db)
    if user_uuid != user.uuid or image.user != user:
        raise HTTPException(status_code=403)

    return get_image_file(image.path)


@router.get(
    "/{user_uuid}/{image_uuid}/transform",
    tags=["images"],
    response_description="Image edit task status",
)
def send_edit_to_celery(
    user_uuid: UUID,
    image_uuid: UUID,
    transform: schemas.Transform,
    db: Session = Depends(get_db),
    user: User = Depends(get_user_or_401),
):
    """Invoke image edit task"""
    image = image_crud.get_image_by_uuid(image_uuid, db)
    if image.user != user:
        raise HTTPException(status_code=403)

    new_filename = Path(settings.file_storage) / "edited" / f"{uuid4()}.png"
    # create directory if doesn't exist, ignore errors
    new_filename.parent.mkdir(parents=True, exist_ok=True)
    # add original image info to transform object
    internal_transform = schemas.TransformInternal(**transform.dict(), original_image_id=image.id)
    task = edit_image.delay(
        input_file=image.path, output_file=new_filename, transform=internal_transform
    )

    task_db = image_crud.create_edit_task(uuid=UUID(task.id), image=image, db=db)
    return {"task_id": task_db.id, "status_url": f"{settings.image_url}/status/{task_db.uuid}"}
