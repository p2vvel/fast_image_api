from sqlalchemy.orm import Session
from fastapi import UploadFile
from pathlib import Path
from uuid import UUID, uuid4
from sqlalchemy import select
from .. import models
from ..config import settings


def get_images(db: Session) -> list[models.Image]:
    all_images = db.query(models.Image).all()
    return all_images


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
