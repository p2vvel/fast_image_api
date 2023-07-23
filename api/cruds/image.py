from sqlalchemy.orm import Session
from fastapi import UploadFile
from pathlib import Path
from uuid import UUID, uuid4
from sqlalchemy import select
from .. import models
from ..config import settings
from celery.result import AsyncResult
from ..tasks.images import app as celery_app


def get_all_images(db: Session) -> list[models.Image]:
    all_images = db.scalars(select(models.Image)).all()
    return all_images


def get_user_images(user: models.User, db: Session) -> list[models.Image]:
    images = db.scalars(select(models.Image).where(models.Image.user == user)).all()
    return images


def create_image(image: UploadFile, user: models.User, db: Session) -> models.Image:
    uuid = uuid4()
    filename = f"{uuid}.{image.filename.split('.')[-1]}"
    new_image = models.Image(original_filename=image.filename, filename=filename, user=user, uuid=uuid)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    new_path = Path(settings.file_storage) / str(user.uuid) / filename
    # do not check if exists, just create and ignore exception exists
    new_path.parent.mkdir(parents=True, exist_ok=True)

    with open(new_path, "wb") as saved_file:
        content = image.file.read()
        saved_file.write(content)

    return new_image


def get_image_by_id(image_id: int, db: Session) -> models.Image:
    image = db.scalar(select(models.Image).where(models.Image.id == image_id))
    return image


def get_image_by_uuid(image_uuid: UUID, db: Session) -> models.Image:
    image = db.scalar(select(models.Image).where(models.Image.uuid == image_uuid))
    return image


def get_celery_task(task_uuid: UUID) -> any:
    '''Get celery task object'''
    task = AsyncResult(str(task_uuid), app=celery_app)
    return task


def get_edit_task(task_uuid: UUID, db: Session) -> models.EditTask:
    '''Get edit task object from database'''
    task = db.scalar(select(models.EditTask).where(models.EditTask.uuid == task_uuid))
    return task


def create_edit_task(uuid: UUID, image: models.Image, db: Session) -> models.EditTask:
    # new_task = models.EditTask(id=None, image=image)
    new_task = models.EditTask(uuid=uuid, image=image)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
