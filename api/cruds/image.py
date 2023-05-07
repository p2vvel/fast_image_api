from sqlalchemy.orm import Session
from fastapi import UploadFile
from pathlib import Path
from uuid import UUID, uuid4
from sqlalchemy import select
from .. import models, config


def get_images(db: Session) -> list[models.Image]:
    all_images = db.query(models.Image).all()
    return all_images


def create_image(image: UploadFile, user: models.User, db: Session) -> models.Image:
    filename = f"{uuid4()}.{image.filename.split('.')[-1]}"
    new_image = models.Image(original_filename=image.filename, filename=filename, user=user)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    new_path = Path(config.FILE_STORAGE) / str(user.uuid) / filename
    new_path.parent.mkdir(exist_ok=True)    # do not check if exists, just create and ignore exception exists

    with open(new_path, "wb") as saved_file:
        content = image.file.read()
        saved_file.write(content)

    return new_image


def get_image_by_uuid(image_uuid: UUID, db: Session) -> models.Image:
    image = db.scalar(select(models.Image).where(models.Image.uuid == image_uuid))
    return image
