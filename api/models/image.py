from api.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..config import IMAGE_URL


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_filename: Mapped[str]
    filename: Mapped[str] = mapped_column(unique=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="images")  # noqa: F821

    original_image_id: Mapped[int | None] = mapped_column(ForeignKey("image.id"), default=None)
    original_image: Mapped["Image"] = relationship()  # noqa: F821

    @property
    def path(self) -> str:
        user_uuid = self.user.uuid
        image_uuid = self.filename.split('.')[0]
        return f"{IMAGE_URL}/{user_uuid}/{image_uuid}"

    def __repr__(self):
        return f"<Image: {self.id}>"
