from fastapi import Depends
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import pytest
import jwt
import pathlib

from .. import config, models
from ..main import app  # noqa: F401
from ..database import Base, get_db
from ..cruds.user import get_user_by_username
from ..utils.crypto import oauth_scheme
from ..utils.crypto import pwd_context

engine = create_engine(config.TEST_DB_URL, connect_args={"check_same_thread": False})
testing_local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    Use different db while testing
    """
    try:
        db = testing_local_session()
        yield db
    finally:
        db.close()


def override_get_user(
    token: str = Depends(oauth_scheme), db: Session = Depends(get_db)
) -> models.User | None:
    """
    Authenticate user by username sent in Bearer
    e.g. 'Bearer pawel' would indicate that 'pawel' is the client,
    for testing purposes only
    """
    if token:
        user = get_user_by_username(token, db)
        return user
    else:
        return None


@pytest.fixture()
def clean_db():
    """
    Fixture created to ensure that there are
    always clean tables in db before every test
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def create_user(
    username: str, password: str = "1234", *, is_superuser: bool = False, is_active: bool = True
) -> models.User:
    """
    Creates new user and returns with given parameters,
    for testing purposes only
    """
    hashed_password = pwd_context.hash(password)  # used passwords' hashes as always
    db = next(override_get_db())
    new_user = models.User(
        username=username, password=hashed_password, is_superuser=is_superuser, is_active=is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def generate_token(username: str, *, expiration_time: timedelta = timedelta(minutes=15)) -> str:
    """
    Generates new jwt token for user with given username,
    for testing purposes only
    """
    payload = {
        "sub": username,
        "iss": expiration_time,
    }
    token = jwt.encode(payload, config.SECRET, algorithm=config.ALGORITHM)
    return token


def auth_header(token: str) -> dict[str, str]:
    """
    Return header with 'Authorization: Bearer <token>' section
    """
    return {"Authorization": f"Bearer {token}"}


TEST_IMAGES_PATH = pathlib.Path("./test_images")
