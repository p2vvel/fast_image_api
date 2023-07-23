from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.responses import FileResponse
from ..config import settings
from pathlib import Path


def get_image_file(image_path: str) -> FileResponse:
    if settings.xsend:
        # Xsendfile implementation
        temp = Path(image_path)
        # construct protected image path (replace base image url to xsend url for internal use)
        xsend_path = Path(settings.xsend_path) / temp.parent.name / temp.name
        header = {"X-Accel-Redirect": str(xsend_path), "Content-Type": "image/png"}
        raise HTTPException(status_code=status.HTTP_200_OK, headers=header)
    else:
        # used for development
        return FileResponse(image_path)
