from sqlalchemy import Column, String, Integer, Boolean
from api.database import Base


class Tier(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    original_image = Column(Boolean, default=False, nullable=False)
    transform = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Tier: '{self.name}'>"