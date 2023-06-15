from fastapi.testclient import TestClient
from api.tests.utils import clean_db  # noqa: F401
from api.tests.utils import app, override_get_db, override_get_user

from api.database import get_db
from api.dependencies.auth import get_user

from ..utils import create_user, auth_header, TEST_IMAGES_PATH

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user


def test_permissions(clean_db):  # noqa: F811
    with TestClient(app) as client:
        create_user("pawel")

        file = {"file": open(TEST_IMAGES_PATH / "avatar1.png", "rb")}
        response = client.post("/images", headers=auth_header("pawel"), files=file)
        assert response.status_code == 201  # logged user can upload image

        response = client.post("/images", files=file)
        assert response.status_code == 401  # anonymous user cannot upload image


def test_upload_save(clean_db):  # noqa: F811
    with TestClient(app) as client:
        create_user("pawel")

        file = {"file": open(TEST_IMAGES_PATH / "avatar1.png", "rb")}
        response = client.post("/images", headers=auth_header("pawel"), files=file)
        assert response.status_code == 201  # logged user can upload image
