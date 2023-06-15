from fastapi.responses import FileResponse
from ..config import settings


# TODO: implement xsendfile - https://www.nginx.com/resources/wiki/start/topics/examples/xsendfile/
def get_image_file(image_path: str) -> FileResponse:
    if settings.environment == "dev":
        return FileResponse(image_path)
    else:
        # TODO: implement Xsendfile
        return FileResponse(image_path)
