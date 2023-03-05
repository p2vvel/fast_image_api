from pydantic import BaseModel


class Image(BaseModel):
    original_filename: str
    filename: str