from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserForm(UserBase):
    password: str


class UserInDB(UserForm):
    active: bool


class UserResponse(UserBase):
    active: bool
