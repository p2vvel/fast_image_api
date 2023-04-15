from pydantic import BaseModel
from datetime import datetime


class TierBase(BaseModel):
    name: str
    original_image: bool
    transform: bool

    class Config:
        orm_mode = True


class TierInDB(TierBase):
    id: int
    created_at: datetime


class TierForm(TierBase):
    pass


class TierResponseAdmin(TierInDB):
    pass


class TierResponseStandard(TierBase):
    pass