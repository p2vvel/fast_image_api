from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..cruds import login as auth_crud


router = APIRouter()


@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> schemas.Token:
    user_db = auth_crud.user_login(user, db)
    token = auth_crud.generate_token(user_db, db)
    return token
