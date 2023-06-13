from pydantic import BaseModel, validator, ValidationError
from uuid import UUID
import datetime
import re
from string import ascii_uppercase, ascii_lowercase, digits, punctuation


def password_validator(cls, value):
    if len(value) < 8:
        raise ValidationError("Password too short (min 8 characters)")
    if len(value) > 250:
        raise ValidationError("Password too long (max 250 characters)")
    if not (any([c in value for c in ascii_lowercase]) and
            any([c in value for c in ascii_uppercase]) and
            any([c in value for c in digits]) and
            any([c in value for c in punctuation])):
        raise ValidationError("Password must contain at least one uppercase letter, one lowercase letter, one digit and one special character") # noqa E501

    return value


class UserBase(BaseModel):
    username: str

    @validator("username")
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValidationError("Username too short (min 3 characters)")
        if len(value) > 20:
            raise ValidationError("Username too long (max 20 characters)")
        if re.match(r"^[a-zA-Z-_\d]+$", value) is None:
            raise ValidationError("Username can only contain letters, numbers, dashes ('-') and underscores ('_')")
        return value

    class Config:
        orm_mode = True


class UserForm(UserBase):
    password: str

    @validator("password")
    def validate_password(cls, value):
        return password_validator(cls, value)


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

    @validator("password")
    def validate_password(cls, value):
        return password_validator(cls, value)
