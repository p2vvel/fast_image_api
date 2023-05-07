from pydantic import BaseModel
from uuid import UUID
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
    is_pro_user: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    uuid: UUID


class UserResponse(UserBase):
    """Same as UserInDB but without password"""

    id: int
    is_active: bool
    is_superuser: bool
    is_pro_user: bool
    uuid: UUID

    # TODO: decide if created_at and updated_at should be sent in response
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserUpdateForm(BaseModel):
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
