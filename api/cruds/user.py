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


def get_user_by_username(username: str, db: Session) -> user_models.User:
    user_db = db.query(user_models.User).filter(
        user_models.User.username == username).first()
    if user_db:
        return user_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def create_user(user: UserForm, db: Session) -> user_models.User:
    hashed_password = pwd_context.hash(user.password)
    user_db = user_models.User(
        username=user.username, password=hashed_password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def delete_user(username: str, db: Session) -> None:
    user_db = get_user_by_username(username, db)
    db.delete(user_db)
    db.commit()
