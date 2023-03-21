from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import crud, schemas
from api.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/test")
def testt():
    return "TESTTEST"


@router.get("/users")
def get_users(db: Session = Depends(get_db)) -> list[schemas.UserResponse]:
    all_users = crud.get_users(db)
    return all_users


@router.post("/users")
def create_user(user: schemas.UserForm, db: Session = Depends(get_db)) -> schemas.UserResponse:
    new_user = crud.create_user(user, db)
    return new_user


@router.delete("/users")
def delete_user(username: str = Body(embed=True), db: Session = Depends(get_db)):
    crud.delete_user(username, db)
    raise HTTPException(status_code=status.HTTP_200_OK)


@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = crud.user_login(user, db)
    token = crud.generate_token(user_db, db)
    return token
