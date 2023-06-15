from fastapi.responses import FileResponse
from ..config import settings


def get_image_file(image_path: str) -> FileResponse:
    if settings.environment == "dev":
        return FileResponse(image_path)
    else:
        # TODO: implement Xsendfile
        pass
        return FileResponse(image_path)
