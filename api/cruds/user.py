from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..models import user as user_models
from ..schemas.user import UserForm

from ..utils.crypto import pwd_context


def get_users(db: Session) -> list[user_models.User]:
    users = db.query(user_models.User).all()
    return users


def get_user_by_username(username: str, db: Session, *, raise_exception=True) -> user_models.User:
    user_db = db.query(user_models.User).filter(
        user_models.User.username == username).first()
    if user_db:
        return user_db
    else:
        if raise_exception:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return None


def create_user(user: UserForm, db: Session) -> user_models.User:
    existing_user = get_user_by_username(user.username, db, raise_exception=False)
    # check if username hasn't been already used
    if existing_user is None:
        hashed_password = pwd_context.hash(user.password)
        user_db = user_models.User(
            username=user.username, password=hashed_password)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db
    else:
        # username has been used preiously
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")


def delete_user(username: str, db: Session) -> None:
    user_db = get_user_by_username(username, db)
    db.delete(user_db)
    db.commit()
