from pydantic import BaseModel
import api.config as config
from pathlib import Path


class Image(BaseModel):
    original_filename: str
    filename: str

    
    class Config:
        orm_mode = True


class OutputImage(Image):
    path: str | None
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.path = Path(config.FILE_STORAGE) / self.filename

    
    class Config:
        orm_mode = True