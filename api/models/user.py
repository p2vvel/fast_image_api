from sqlalchemy.orm import mapped_column, relationship, Mapped
from api.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_pro_user: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())

    images: Mapped[list["Image"]] = relationship(back_populates="user")     # noqa: F821

    def __repr__(self):
        return f"<User: '{self.username}'>"
