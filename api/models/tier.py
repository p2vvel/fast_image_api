from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database import Base
from datetime import datetime


class Tier(Base):
    __tablename__ = "tier"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    original_image: Mapped[bool] = mapped_column(default=False)
    transform: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    users: Mapped[list["User"]] = relationship(back_populates="tier")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Tier: '{self.name}'>"
