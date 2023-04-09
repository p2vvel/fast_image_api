from fastapi.testclient import TestClient
from api.tests.utils import (
    clean_db,
    app,
    override_get_db,
    create_user,
    override_get_user,
    auth_header,
)
from api import models
from api.database import get_db
from api.dependencies.auth import get_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user
client = TestClient(app)


def test_user_delete(clean_db):
    pawel = create_user("pawel")
    admin = create_user("admin", is_superuser=True)
    db = next(override_get_db())
    all_users = lambda: db.query(models.User).all()

    assert len(all_users()) == 2  # 2 users in db
    response = client.delete("/users/pawel", headers=auth_header("pawel"))
    assert response.status_code == 200
    assert len(all_users()) == 1  # 1 user in db, 'pawel' has been killed

    pawel = create_user("pawel")  # create another 'pawel'
    response = client.delete("/users/admin", headers=auth_header("pawel"))
    assert response.status_code == 401

    # admin can delete everything
    response = client.delete("/users/pawel", headers=auth_header("admin"))
    assert response.status_code == 200
    response = client.delete("/users/admin", headers=auth_header("admin"))
    assert response.status_code == 200

    assert len(all_users()) == 0  # all users have been deleted
