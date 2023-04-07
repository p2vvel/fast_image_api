from pydantic import BaseModel
import datetime


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserForm(UserBase):
    password: str


class UserInDB(UserForm):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserResponse(UserBase):
    '''Same as UserInDB but without password'''
    id: int
    is_active: bool
    is_superuser: bool
    # TODO: decide if created_at and updated_at should be sent in response
    created_at: datetime.datetime       
    updated_at: datetime.datetime
