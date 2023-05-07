from PIL import Image
from ..schemas import transform as schema


def change_orientation(img: Image, flip: schema.Rotation) -> Image:
    """Flip image according to flip value"""
    match flip:
        case schema.Flip.NONE:
            return img
        case schema.Flip.HORIZONTAL:
            return img.transpose(Image.FLIP_LEFT_RIGHT)
        case schema.Flip.VERTICAL:
            return img.transpose(Image.FLIP_TOP_BOTTOM)
        case schema.Flip.BOTH:
            # mirroring and flipping is the same as rotating by 180 degrees
            return img.transpose(Image.ROTATE_180)
        case _:
            raise ValueError("Invalid flip value")
