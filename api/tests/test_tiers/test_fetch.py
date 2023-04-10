from fastapi.testclient import TestClient
from api.tests.utils import clean_db, app, override_get_db, override_get_user
from api import models
from api.database import get_db
from api.dependencies.auth import get_user
import datetime
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
    assert response.status_code == 401


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
    assert response.status_code == 401


def test_fetch(clean_db):
    db = next(override_get_db())
    create_user("admin", is_superuser=True)
    header = auth_header("admin")
    then = datetime.datetime.now()
    input = {"name": "abc", "original_image": False, "transform": False}
    tier = models.Tier(**input)
    db.add(tier)
    db.commit()
    db.refresh(tier)

    response = client.get("/tiers/abc", headers=header)
    assert response.status_code == 200
    json = response.json()
    assert set(json.keys()) == {"id", "name", "original_image", "transform", "created_at"}
    for key in input:
        assert input[key] == json[key]
    assert isinstance(json["id"], int)
    created_at = datetime.datetime.fromisoformat(json["created_at"])
    assert then - created_at < datetime.timedelta(seconds=5)
