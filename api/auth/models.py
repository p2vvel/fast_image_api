from sqlalchemy import Column, String, Integer, Boolean
from api.database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)#, unique=True,)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)