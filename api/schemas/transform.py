from pydantic import BaseModel
from enum import Enum


class Rotation(int, Enum):
    NONE = 0
    ROTATE_90 = 90
    ROTATE_180 = 180
    ROTATE_270 = 270


class Flip(str, Enum):
    NONE = "none"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    BOTH = "both"


class Transform(BaseModel):
    rotation: Rotation = Rotation.NONE
    flip: Flip = Flip.NONE
