from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from ..database import get_db

from .. import schemas


from ..cruds import user as user_crud
from ..dependencies.auth import get_user_or_401

router = APIRouter()


@router.get("/")
def get_users(
    db: Session = Depends(get_db), user: schemas.UserInDB = Depends(get_user_or_401)
) -> list[schemas.UserResponse]:
    if user.is_superuser:
        # admin can get all users
        user = user_crud.get_users(db)
        return user
    else:
        # standard users can only fetch theirselves
        user = [user_crud.get_user_by_username(user.username, db)]
        return user


@router.get("/{username}")
def get_users(
    username: str, db: Session = Depends(get_db), user: schemas.UserInDB = Depends(get_user_or_401)
) -> schemas.UserResponse:
    if user.is_superuser or user.username == username:
        user = user_crud.get_user_by_username(username, db)
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/")
def create_user(user: schemas.UserForm, db: Session = Depends(get_db)) -> schemas.UserResponse:
    new_user = user_crud.create_user(user, db)
    return new_user


@router.patch("/{username}")
def update_user(
    username: str,
    new_data: schemas.UserUpdateForm = Body(),
    db: Session = Depends(get_db),
    user: schemas.UserInDB = Depends(get_user_or_401),
) -> schemas.UserResponse:
    if user.is_superuser:
        # no need to change anything, admin can change whole profile
        updated_user = user_crud.update_user(username, new_data, db)
        return updated_user
    elif user.username == username:
        # 'standard' users can change only password
        filtered_new_data = schemas.UserUpdateForm(password=new_data.password)
        updated_user = user_crud.update_user(username, filtered_new_data, db)
        return updated_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.delete("/{username}")
def delete_user(
    username: str, db: Session = Depends(get_db), user: schemas.UserInDB = Depends(get_user_or_401)
) -> None:
    if user.is_superuser or user.username == username:
        user_crud.delete_user(username, db)
        raise HTTPException(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
