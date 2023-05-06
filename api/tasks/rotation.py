from PIL import Image
from ..schemas import transform as schema


def change_rotation(img: Image, rotation: schema.Rotation) -> Image:
    """Rotate image according to rotation value"""
    match rotation:
        case schema.Rotation.NONE:
            return img
        case schema.Rotation.ROTATE_90:
            return img.transpose(Image.ROTATE_270)  # PIL rotates counter-clockwise
        case schema.Rotation.ROTATE_180:
            return img.transpose(Image.ROTATE_180)
        case schema.Rotation.ROTATE_270:
            return img.transpose(Image.ROTATE_90)   # PIL rotates counter-clockwise
        case _:
            raise ValueError("Invalid rotation value")
