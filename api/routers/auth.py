from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db

from .. import schemas
from ..models import user as user_models


from ..cruds import user as user_crud, login as auth_crud
from ..dependencies.auth import get_user, get_user_or_401


router = APIRouter()


@router.get("/users")
def get_users(db: Session = Depends(get_db), user: schemas.UserInDB = Depends(get_user_or_401)) -> list[schemas.UserResponse]:
    if user.is_superuser:
        # admin can get all users
        user = user_crud.get_users(db)
        return user
    else:
        # normal users can only fetch itself
        user = [user_crud.get_user_by_username(user.username, db)]
        return user


@router.post("/users")
def create_user(user: schemas.UserForm, db: Session = Depends(get_db)) -> schemas.UserResponse:
    new_user = user_crud.create_user(user, db)
    return new_user


@router.delete("/users")
def delete_user(username: str = Body(embed=True), db: Session = Depends(get_db)):
    user_crud.delete_user(username, db)
    raise HTTPException(status_code=status.HTTP_200_OK)


@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = auth_crud.user_login(user, db)
    token = auth_crud.generate_token(user_db, db)
    return token
