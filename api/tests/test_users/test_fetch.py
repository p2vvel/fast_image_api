from fastapi.testclient import TestClient
from api.tests.utils import clean_db  # noqa: F401
from api.tests.utils import app, override_get_db, create_user, override_get_user, auth_header
from api.database import get_db
from api.dependencies.auth import get_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user
client = TestClient(app)


def test_all_user_fetch(clean_db):
    # create sample users
    create_user("pawel")
    create_user("admin", is_superuser=True)
    create_user("kamilek")

    # check anonymous user
    response = client.get("/users")
    assert response.status_code == 401  # endpoint not availabe

    response = client.get("/users", headers=auth_header("pawel"))
    assert response.status_code == 200
    assert len(response.json()) == 1  # only one user
    assert response.json()[0]["username"] == "pawel"  # 'pawel' alone

    response = client.get("/users", headers=auth_header("admin"))
    assert response.status_code == 200
    assert len(response.json()) == 3  # all users
    # sets comparisions is easier because they are unordered:
    assert {k["username"] for k in response.json()} == {"admin", "pawel", "kamilek"}


def test_user_fetch(clean_db):
    create_user("pawel")
    create_user("admin", is_superuser=True)

    response = client.get("/users/pawel")
    assert response.status_code == 401
    response = client.get("/users/admin", headers=auth_header("pawel"))
    assert response.status_code == 401
    response = client.get("/users/pawel", headers=auth_header("pawel"))
    assert response.status_code == 200
    assert response.json().get("username") == "pawel"

    response = client.get("/users/pawel", headers=auth_header("admin"))
    assert response.status_code == 200
    assert response.json().get("username") == "pawel"

    response = client.get("/users/admin", headers=auth_header("admin"))
    assert response.status_code == 200
    assert response.json().get("username") == "admin"
