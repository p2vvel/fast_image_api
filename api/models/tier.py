from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database import Base


class Tier(Base):
    __tablename__ = "tier"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    original_image: Mapped[bool] = mapped_column(default=False)
    transform: Mapped[bool] = mapped_column(default=False)

    users: Mapped[list["User"]] = relationship(back_populates="tier")

    def __repr__(self) -> str:
        return f"<Tier: '{self.name}'>"
