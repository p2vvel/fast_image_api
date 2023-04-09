from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
import datetime

from ..schemas.user import UserForm, UserUpdateForm
from ..models.user import User


from ..utils.crypto import pwd_context


def get_users(db: Session) -> list[User]:
    users = db.scalars(select(User)).all()
    return users


def get_user_by_username(username: str, db: Session, *, raise_exception=True) -> User:
    try:
        user_db = db.scalars(select(User).where(User.username == username)).one()
        return user_db
    except NoResultFound:
        if raise_exception:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            return None


def create_user(user: UserForm, db: Session) -> User:
    existing_user = get_user_by_username(user.username, db, raise_exception=False)
    # check if username hasn't already been used
    if existing_user is None:
        hashed_password = pwd_context.hash(user.password)
        user_db = User(username=user.username, password=hashed_password)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db
    else:
        # username has been used preiously
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")


def update_user(username: str, new_data: UserUpdateForm, db: Session) -> User:
    try:
        user = db.scalars(select(User).where(User.username == username)).one()
        new_data_dict = new_data.dict(exclude_unset=True)
        for key in new_data_dict:
            setattr(user, key, new_data_dict[key])
        user.updated_at = datetime.datetime.now()
        db.commit()
        return user
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def delete_user(username: str, db: Session) -> None:
    user_db = get_user_by_username(username, db)
    db.delete(user_db)
    db.commit()
