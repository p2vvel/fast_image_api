from pydantic import BaseModel


class Token(BaseModel):
    active_token: str
    token_type: str = "bearer"
    expires: int
