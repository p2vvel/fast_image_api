from fastapi.testclient import TestClient
from api.tests.utils import clean_db  # noqa: F401
from api.tests.utils import app, override_get_db, create_user, override_get_user, auth_header

from api import models
from api.database import get_db
from api.dependencies.auth import get_user
import datetime
import time


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user


def test_standard_user_update(clean_db):
    with TestClient(app) as client:    
        db = next(override_get_db())
        username = "pawel"
        create_user(username, "Dupa1234.")
        new_data = {
            "password": "New_password1234.",
            "is_active": False,
            "is_superuser": True,
        }
        get_user = (
            lambda: db.query(models.User).filter(models.User.username == username).first()
        )  # noqa: E731

        # convert to dict to prevent from querying db after update, thus getting already updated data
        old_user_data = get_user().__dict__
        response = client.patch(f"/users/{username}", headers=auth_header(username), json=new_data)
        assert response.status_code == 200
        new_standard_user = get_user()

        # password can be changed by user
        assert old_user_data["password"] != new_standard_user.password
        # 'standard' user can only change password
        assert old_user_data["is_active"] == new_standard_user.is_active
        assert old_user_data["is_superuser"] == new_standard_user.is_superuser


def test_standard_user_update_unauthorized(clean_db):
    with TestClient(app) as client:
        db = next(override_get_db())
        username = "pawel"
        create_user(username, "Dupa1234.")
        new_data = {
            "password": "new password",
            "is_active": False,
            "is_superuser": True,
        }
        get_user = (
            lambda: db.query(models.User).filter(models.User.username == username).first()
        )  # noqa: E731

        # converting to dict to prevent from querying db after update, thus getting already updated data
        old_user_data = get_user().__dict__
        response = client.patch(f"/users/{username}", json=new_data)
        assert response.status_code == 401
        new_standard_user = get_user()
        # no changes:
        assert old_user_data["password"] == new_standard_user.password
        assert old_user_data["is_active"] == new_standard_user.is_active
        assert old_user_data["is_superuser"] == new_standard_user.is_superuser


def test_standard_user_update_other_user(clean_db):
    with TestClient(app) as client:
        db = next(override_get_db())
        username = "pawel"
        username_2 = "kamilek"
        create_user(username, "Dupa1234.")
        create_user(username_2, "Dupa1234.")
        new_data = {
            "password": "New_password1234.",
            "is_active": False,
            "is_superuser": True,
        }
        get_user = (
            lambda: db.query(models.User).filter(models.User.username == username).first()
        )  # noqa: E731

        # converting to dict to prevent from querying db after update, thus getting already updated data
        old_user_data = get_user().__dict__
        response = client.patch(f"/users/{username}", headers=auth_header(username_2), json=new_data)
        assert response.status_code == 401
        new_standard_user = get_user()
        # no changes
        assert old_user_data["password"] == new_standard_user.password
        assert old_user_data["is_active"] == new_standard_user.is_active
        assert old_user_data["is_superuser"] == new_standard_user.is_superuser


def test_superuser_update(clean_db):
    with TestClient(app) as client:
        db = next(override_get_db())
        username = "pawel"
        create_user(username, "Dupa1234.")
        create_user("admin", "Dupa1234.", is_superuser=True)
        new_data = {
            "password": "New_password1234.",
            "is_active": False,
            "is_superuser": True,
        }
        get_user = (
            lambda: db.query(models.User).filter(models.User.username == username).first()
        )  # noqa: E731

        # converting to dict to prevent from querying db after update, thus getting already updated data
        old_user_data = get_user().__dict__
        response = client.patch(f"/users/{username}", headers=auth_header("admin"), json=new_data)
        assert response.status_code == 200
        new_standard_user = get_user()

        # superuser can change everything
        assert old_user_data["password"] != new_standard_user.password
        assert old_user_data["is_active"] != new_standard_user.is_active
        assert old_user_data["is_superuser"] != new_standard_user.is_superuser


def test_updated_at_change(clean_db):
    with TestClient(app) as client:
        create_user("pawel", "Dupa1234.")

        response = client.get("/users/pawel", headers=auth_header("pawel"))
        assert response.status_code == 200
        old_updated_at = datetime.datetime.fromisoformat(response.json().get("updated_at"))

        time.sleep(1)  # wait 1 second to show difference

        response = client.patch("/users/pawel", headers=auth_header("pawel"), json={"password": "Dupa12345."})
        assert response.status_code == 200
        new_updated_at = datetime.datetime.fromisoformat(response.json().get("updated_at"))

        assert new_updated_at - old_updated_at > datetime.timedelta(seconds=1)
