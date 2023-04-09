from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import datetime

from ..models import user as user_models
from ..schemas.user import UserForm, UserUpdateForm


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


def update_user(username: str, new_data: UserUpdateForm, db: Session) -> user_models.User:
    user_query = db.query(user_models.User).filter(user_models.User.username == username)   # get user instances by now

    # raise 404 if there are no users with such nicknames
    if len(user_query.all()) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        new_data_dict = new_data.dict(exclude_unset=True)
        new_data_dict["updated_at"] = datetime.datetime.now()
        user_query.update(new_data_dict)
        db.commit()
        updated_user = user_query.first()
        return updated_user


def delete_user(username: str, db: Session) -> None:
    user_db = get_user_by_username(username, db)
    db.delete(user_db)
    db.commit()
