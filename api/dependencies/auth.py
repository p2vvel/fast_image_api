from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.crypto import oauth_scheme
from ..cruds.user import get_user_by_username
from .. import models
from ..config import settings
from ..database import get_db
import jwt


def get_user(
    token: str = Depends(oauth_scheme), db: Session = Depends(get_db)
) -> models.User | None:
    if token:
        payload = jwt.decode(token, settings.secret, algorithms=[settings.algorithm])
        username = payload.get("sub")
        user = get_user_by_username(username, db)
        return user
    else:
        return None


def get_user_or_401(user: models.User | None = Depends(get_user)) -> models.User:
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_admin_or_401(user: models.User | None = Depends(get_user_or_401)) -> models.User:
    if user.is_superuser:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
