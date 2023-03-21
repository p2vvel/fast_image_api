from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from api.database import get_db
from api.auth import models, schemas
import api.config as config
import jwt
import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_users(db: Session) -> list[models.User]:
    users = db.query(models.User).all()
    return users


def get_user_by_username(username: str, db: Session) -> models.User:
    user_db = db.query(models.User).filter(
        models.User.username == username).first()
    if user_db:
        return user_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def create_user(user: schemas.UserForm, db: Session) -> models.User:
    hashed_password = pwd_context.hash(user.password)
    user_db = models.User(username=user.username, password=hashed_password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def delete_user(username: str, db: Session) -> None:
    user_db = get_user_by_username(username, db)
    db.delete(user_db)
    db.commit()


def user_login(user: OAuth2PasswordRequestForm, db: Session) -> models.User:
    user_db = db.query(models.User).filter(
        models.User.username == user.username).first()

    if user_db:
        if pwd_context.verify(user.password, user_db.password):
            return user_db
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User '{user.username}' not existing")


def generate_token(user: schemas.UserBase, db: Session, time_delta: datetime.timedelta = datetime.timedelta(minutes=15)) -> schemas.Token:
    expiration_time = (datetime.datetime.utcnow() + time_delta).timestamp()
    payload = {
        "sub": user.username,
        "iss": expiration_time,
    }

    token = jwt.encode(payload, config.SECRET, algorithm=config.ALGORITHM)
    return schemas.Token(active_token=token, expires=expiration_time)


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)) -> models.User | None:
    if token:
        payload = jwt.decode(
            token,
            config.SECRET,
            algorithms=[config.ALGORITHM]
        )
        username = payload.get("sub")
        user = get_user_by_username(username, db)
        return user
    else:
        return None
