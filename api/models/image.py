from api.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID
from pathlib import Path
from api.config import settings


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

    edit_tasks: Mapped[list["EditTask"]] = relationship(back_populates="image")  # noqa: F821

    @property
    def url(self) -> str:
        user_uuid = self.user.uuid
        image_uuid = self.uuid
        return f"{settings.image_url}/{user_uuid}/{image_uuid}"

    @property
    def path(self) -> Path:
        return Path(settings.file_storage) / str(self.user.uuid) / self.filename

    def __repr__(self):
        return f"<Image: {self.id}>"


class EditTask(Base):
    __tablename__ = "edit_task"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(unique=True, nullable=False, index=True)

    image_id: Mapped[int] = mapped_column(ForeignKey("image.id"))
    image: Mapped["Image"] = relationship(back_populates="edit_tasks")  # noqa: F821
