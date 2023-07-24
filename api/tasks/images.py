from celery import Celery
from PIL import Image
from ..schemas import transform as schema
from .colors import change_colors
from .rotation import change_rotation
from .orientation import change_orientation
from .size import change_size
from api.config import settings


app = Celery("tasks", broker=settings.celery_broker, backend=settings.celery_backend)
app = Celery("tasks", broker=settings.celery_broker, backend=settings.celery_backend)
# WARNING:
# It might not be the best idea to send pickled data, but I decided to limit database queries
# Passing tasks and results might be done by sending only IDs of arguments/results saved in DB,
# but I decided to leave it as it is - project made for learning purposes
app.conf.update(
    task_serializer='pickle',
    result_serializer='pickle',
    accept_content=['pickle'],
    result_extended=True
)


@app.task
def edit_image(input_file: str, output_file: str, transform: schema.TransformInternal) -> None:
    with Image.open(input_file) as image:
        img = image
        img = change_rotation(img, transform.rotation)
        img = change_orientation(img, transform.flip)
        img = change_colors(img, transform.color)
        img = change_size(img, transform.size)
        img.save(output_file)
        return output_file


if __name__ == "__main__":
    transformation = schema.Transform(
        rotation=schema.Rotation.NONE,
        flip=schema.Flip.NONE,
        color=schema.Color.SEPIA,
        size=schema.Size(x=0, y=200),
    )
    edit_image("./test_images/avatar1.png", "avatar1_bw.png", transformation)
