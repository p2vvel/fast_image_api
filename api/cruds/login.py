from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import datetime
import jwt

from ..database import get_db
from ..utils.crypto import pwd_context, oauth_scheme
from .. import schemas, models, config


def user_login(user: OAuth2PasswordRequestForm, db: Session) -> models.User:
    user_db = db.query(models.User).filter(models.User.username == user.username).first()

    if user_db:
        if pwd_context.verify(user.password, user_db.password):
            return user_db
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{user.username}' not existing"
        )


def generate_token(
    user: schemas.UserBase,
    db: Session,
    time_delta: datetime.timedelta = datetime.timedelta(minutes=15),
) -> schemas.Token:
    expiration_time = (datetime.datetime.utcnow() + time_delta).timestamp()
    payload = {
        "sub": user.username,
        "iss": expiration_time,
    }

    token = jwt.encode(payload, config.SECRET, algorithm=config.ALGORITHM)
    return schemas.Token(active_token=token, expires=expiration_time)
