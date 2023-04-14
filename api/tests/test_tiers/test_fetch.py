from fastapi.testclient import TestClient
from api.tests.utils import clean_db  # noqa: F401
from api.tests.utils import app, override_get_db, override_get_user
from api import models
from api.database import get_db
from api.dependencies.auth import get_user
from ..utils import create_user, auth_header
from ... import models

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user
client = TestClient(app)


def test_fetch_all_permissions(clean_db):
    username = "pawel"
    create_user(username)

    # unlogged don't have an access
    response = client.get("/tiers")
    assert response.status_code == 401
    # 'standard' users don't have an access
    response = client.get("/tiers", headers=auth_header(username))
    assert response.status_code == 200


def test_fetch_permissions(clean_db):
    db = next(override_get_db())
    username = "pawel"
    create_user(username)
    tier = models.Tier(name="abc", original_image=False, transform=False)
    db.add(tier)
    db.commit()
    db.refresh(tier)

    # unlogged don't have an access
    response = client.get("/tiers/abc")
    assert response.status_code == 401
    # 'standard' users don't have an access
    response = client.get("/tiers/abc", headers=auth_header(username))
    assert response.status_code == 200


def test_fetch_admin(clean_db):
    # db = next(override_get_db())
    create_user("admin", is_superuser=True)
    header = auth_header("admin")
    input = {"name": "abc", "original_image": False, "transform": False}

    create_response = client.post(url="/tiers", headers=header, json=input)
    assert create_response.status_code == 200

    response_one = client.get("/tiers/abc", headers=header)
    assert response_one.status_code == 200
    assert (
        create_response.json() == response_one.json()
    )  # create endpoint is already checked and they (should) return the same data

    response_all = client.get("/tiers", headers=header)
    assert response_all.status_code == 200
    assert [create_response.json()] == response_all.json()


def test_fetch_standard_user(clean_db):
    # db = next(override_get_db())
    create_user("pawel")
    create_user("admin", is_superuser=True)

    admin_header = auth_header("admin")
    pawel_header = auth_header("pawel")
    input = {"name": "abc", "original_image": False, "transform": False}

    create_response = client.post(url="/tiers", headers=admin_header, json=input)
    assert create_response.status_code == 200

    response_one = client.get("/tiers/abc", headers=pawel_header)
    assert response_one.status_code == 200
    assert (
        input == response_one.json()
    )  # create endpoint is already checked and they (should) return the same data

    response_all = client.get("/tiers", headers=pawel_header)
    assert response_all.status_code == 200
    assert [input] == response_all.json()
