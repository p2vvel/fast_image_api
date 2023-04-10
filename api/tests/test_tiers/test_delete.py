from fastapi.testclient import TestClient
from api.tests.utils import clean_db, app, override_get_db, override_get_user
from api import models
from api.database import get_db
from api.dependencies.auth import get_user

from ..utils import create_user, auth_header
from ... import models

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user
client = TestClient(app)


def test_delete_permissions(clean_db):
    username = "pawel"
    create_user(username)

    # unlogged don't have an access
    response = client.get("/tiers")
    assert response.status_code == 401
    # 'standard' users don't have an access
    response = client.get("/tiers", headers=auth_header(username))
    assert response.status_code == 401


def test_delete(clean_db):
    db = next(override_get_db())
    create_user("admin", is_superuser=True)
    header = auth_header("admin")
    names = ("abc", "def", "xyz")

    # create some tiers
    for k in names:
        input = {"name": k, "original_image": False, "transform":False}
        tier = models.Tier(**input)
        db.add(tier)
    db.commit()
    db.refresh(tier)

    all = db.query(models.Tier).all()
    assert {k.name for k in all} == set(names)

    response = client.delete("/tiers/def", headers=header) # deleting "def" tier
    assert response.status_code == 200
    filtered = db.query(models.Tier).all()
    assert {k.name for k in filtered} == {"abc", "xyz"}  # "def" has been deleted
    