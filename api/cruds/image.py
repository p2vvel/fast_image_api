from sqlalchemy.orm import Session
from fastapi import UploadFile
from pathlib import Path
import uuid

from .. import models, config, schemas


def get_images(db: Session) -> list[schemas.Image]:
    all_images = db.query(models.Image).all()
    return all_images


def create_image(image: UploadFile, user: models.User, db: Session) -> schemas.Image:
    filename = f"{uuid.uuid4()}.{image.filename.split('.')[-1]}"
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
