from sqlalchemy.orm import Session
from api import models, schemas


def get_images(db: Session) -> list[schemas.Image]:
    all_images = db.query(models.Image).all()
    return all_images