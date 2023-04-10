from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey
from api.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    tier_id: Mapped[int | None] = mapped_column(ForeignKey("tier.id"), default=None)
    tier: Mapped["Tier"] = relationship(back_populates="users")

    def __repr__(self):
        return f"<User: '{self.username}'>"
