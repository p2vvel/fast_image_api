from pydantic import BaseModel


class TierBase(BaseModel):
    name: str
    original_image: bool
    transform: bool

    class Config:
        orm_mode = True


class TierInDB(TierBase):
    id: int


class TierForm(TierBase):
    pass


class TierResponse(TierInDB):
    pass
