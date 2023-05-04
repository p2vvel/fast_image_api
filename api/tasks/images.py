from celery import Celery
from PIL import Image, ImageOps
from ..schemas import transform as schema


app = Celery('tasks', broker='redis://', backend='redis://')


@app.task
def edit_image(input_file: str, output_file: str, transform: schema.Transform):
    with Image.open(input_file) as image:
        img = image
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


def change_colors(img: Image, color: schema.Color):
    """Change image colors according to color value"""
    match color:
        case schema.Color.NONE:
            return img
        case schema.Color.BLACK_AND_WHITE:
            return ImageOps.grayscale(img)
        case schema.Color.SEPIA:
            result = img.copy()
            pixels = result.load()
            width, height = img.size
            for px in range(width):
                for py in range(height):
                    r, g, b = pixels[px, py]
                    newR = int(r * 0.393 + g * 0.769 + b * 0.189)
                    newG = int(r * 0.349 + g * 0.686 + b * 0.168)
                    newB = int(r * 0.272 + g * 0.534 + b * 0.131)
                    pixels[px, py] = (newR, newG, newB)
            return result
        case schema.Color.NEGATIVE:
            return ImageOps.invert(img)
        case schema.Color.WARM:
            ratio = 15
            result = img.copy()
            pixels = result.load()
            width, height = img.size
            for px in range(width):
                for py in range(height):
                    r, g, b = pixels[px, py]
                    pixels[px, py] = (r + ratio, g, b - ratio)
            return result
        case schema.Color.COLD:
            ratio = 15
            result = img.copy()
            pixels = result.load()
            width, height = img.size
            for px in range(width):
                for py in range(height):
                    r, g, b = pixels[px, py]
                    pixels[px, py] = (r - ratio, g, b + ratio)
            return result
        case _:
            raise ValueError("Invalid color value")


if __name__ == "__main__":
    # transformation = schema.Transform(rotation=schema.Rotation.NONE, flip=schema.Flip.NONE)
    # edit_image("./test_images/avatar1.png", "avatar1_bw.png", transformation)
    img = Image.open("./test_images/avatar1.png")
    img = change_colors(img, schema.Color.COLD)
    # img = change_colors(img, schema.Color.NONE)
    img.save("avatar1_bw.png")
