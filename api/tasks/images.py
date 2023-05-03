from celery import Celery
from PIL import Image
from ..schemas import transform as schema


app = Celery('tasks', broker='redis://', backend='redis://')


@app.task
def edit_image(input_file: str, output_file: str, transform: schema.Transform):
    with Image.open(input_file) as image:
        img = image.convert("L")
        img = rotate_image(img, transform.rotation)
        img = flip_image(img, transform.flip)
        img.save(output_file)


def rotate_image(img: Image, rotation: schema.Rotation):
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


def flip_image(img: Image, flip: schema.Rotation):
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


if __name__ == "__main__":
    transformation = schema.Transform(rotation=schema.Rotation.NONE, flip=schema.Flip.NONE)
    edit_image("./test_images/avatar1.png", "avatar1_bw.png", transformation)
