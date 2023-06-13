from pydantic import BaseModel


class Image(BaseModel):
    original_filename: str
    filename: str

    class Config:
        orm_mode = True


class OutputImage(Image):
    url: str | None

    class Config:
        orm_mode = True
