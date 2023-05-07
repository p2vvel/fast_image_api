from PIL import Image
from ..schemas import transform as schema


def change_size(img: Image, size: schema.Size) -> Image:
    """Change image size according to size value"""
    if size.x == size.y == 0:
        return img      # don't resize if both dimensions are 0
    elif size.x != 0 and size.y != 0:
        return img.resize((size.x, size.y))
    else:
        x, y = img.size
        ratio = x / y
        if size.x != 0:
            return img.resize((size.x, int(size.x / ratio)))
        else:
            return img.resize((int(size.y * ratio), size.y))
