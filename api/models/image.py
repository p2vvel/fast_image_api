from api.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..config import IMAGE_URL, FILE_STORAGE
from uuid import uuid4, UUID
from pathlib import Path

class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(unique=True, nullable=False, index=True)
    original_filename: Mapped[str]
    filename: Mapped[str] = mapped_column(unique=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="images")  # noqa: F821

    original_image_id: Mapped[int | None] = mapped_column(ForeignKey("image.id"), default=None)
    original_image: Mapped["Image"] = relationship()  # noqa: F821

    @property
    def url(self) -> str:
        user_uuid = self.user.uuid
        image_uuid = self.uuid
        return f"{IMAGE_URL}/{user_uuid}/{image_uuid}"

    @property
    def path(self) -> Path:
        return Path(FILE_STORAGE) / str(self.user.uuid) / self.filename

    def __repr__(self):
        return f"<Image: {self.id}>"
