from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from ..main import app
from ..database import Base, get_db
from .. import config


engine = create_engine(config.TEST_DB_URL, connect_args={"check_same_thread": False})
testing_local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = testing_local_session()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
