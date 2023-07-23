from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from ..database import get_db

from .. import schemas


from ..cruds import user as user_crud
from ..dependencies.auth import get_user_or_401

router = APIRouter()


@router.get("/", tags=["auth"], response_description="Users data")
def get_users(
    db: Session = Depends(get_db), user: schemas.UserInDB = Depends(get_user_or_401)
) -> list[schemas.UserResponse]:
    '''Fetch users data. Admin can get all users, standard users can get only fetch their own data'''
    if user.is_superuser:
        # admin can get all users
        user = user_crud.get_users(db)
        return user
    else:
        # standard users can only fetch theirselves
        user = [user_crud.get_user_by_username(user.username, db)]
        return user


@router.get("/{username}", tags=["auth"])
def get_user(
    username: str, db: Session = Depends(get_db), user: schemas.UserInDB = Depends(get_user_or_401)
) -> schemas.UserResponse:
    if user.is_superuser or user.username == username:
        user = user_crud.get_user_by_username(username, db)
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/", tags=["auth"], status_code=status.HTTP_201_CREATED, response_description="Created user")  # noqa: #501
def create_user(user: schemas.UserForm, db: Session = Depends(get_db)) -> schemas.UserResponse:
    '''Create new user'''
    new_user = user_crud.create_user(user, db)
    return new_user


@router.patch("/{username}", tags=["auth"], response_description="Updated user")
def update_user(
    username: str,
    new_data: schemas.UserUpdateForm = Body(),
    db: Session = Depends(get_db),
    user: schemas.UserInDB = Depends(get_user_or_401),
) -> schemas.UserResponse:
    '''Update user data. Admin can change whole profile, standard users can only change password'''
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


@router.delete("/{username}", tags=["auth"], status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    username: str, db: Session = Depends(get_db), user: schemas.UserInDB = Depends(get_user_or_401)
) -> None:
    '''Delete user. Admin can delete any user, standard users can only delete their own profile'''
    if user.is_superuser or user.username == username:
        user_crud.delete_user(username, db)
        # raise HTTPException(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
