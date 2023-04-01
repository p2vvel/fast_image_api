from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db

from .. import schemas
from ..models import user as user_models


from ..cruds import user as user_crud, login as auth_crud
from ..cruds.login import get_current_user


router = APIRouter()


@router.get("/test")
def test(user: user_models.User | None = Depends(get_current_user)):
    if user:
        return f"Hi, {user.username}!"
    else:
        return f"Hi, stranger!"


@router.get("/users")
def get_users(db: Session = Depends(get_db)) -> list[schemas.UserResponse]:
    all_users = user_crud.get_users(db)
    return all_users


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
