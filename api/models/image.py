from sqlalchemy import Column, String, Integer
from api.database import Base


class Image(Base):
    __tablename__ = "Images"

    id = Column(Integer, primary_key=True)
    original_filename = Column(String)
    filename = Column(String, unique=True)
