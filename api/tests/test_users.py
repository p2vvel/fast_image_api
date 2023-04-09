from fastapi.testclient import TestClient
from .utils import clean_db, app, override_get_db, create_user, override_get_user, auth_header
from .. import models
from ..database import get_db
from ..dependencies.auth import get_user
import datetime
import time


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_user] = override_get_user
client = TestClient(app)


def test_user_create(clean_db):
    response = client.post("/users", json={"username": "pawel", "password": "1234"})
    assert response.status_code == 200

    json = response.json()
    assert json.get("username") == "pawel"
    assert json.get("is_superuser") == False
    assert json.get("is_active") == True
    # there should be no password sent in response
    assert "password" not in json
    # TODO: is it good idea to test it? might be dependable on db engine
    assert json.get("id") == 1
    # creation and update times should be equal at the creation
    # moment, although there are some minor differences in
    # miliseconds due to default values being taken separately
    created_at = datetime.datetime.fromisoformat(json.get("created_at"))
    updated_at = datetime.datetime.fromisoformat(json.get("updated_at"))
    assert updated_at - created_at < datetime.timedelta(seconds=0.1)


def test_create_user_wrong_input(clean_db):
    # normal user creation
    response = client.post("/users", json={"username": "pawel", "password": "1234"})
    assert response.status_code == 200

    # create duplicated username
    response = client.post("/users", json={"username": "pawel", "password": "1234"})
    assert response.status_code == 409  # endpoint should return 409 (duplicate)

    # create user without password
    response = client.post("/users", json={"username": "pawel2"})
    assert response.status_code == 422

    # create user without username
    response = client.post("/users", json={"username": "pawel3"})
    assert response.status_code == 422

    db = next(override_get_db())  # get db to test its content
    assert len(db.query(models.User).all()) == 1  # only first user was created


def test_all_user_fetch(clean_db):
    # create sample users
    pawel = create_user("pawel")
    admin = create_user("admin", is_superuser=True)
    kamilek = create_user("kamilek")

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
    pawel = create_user("pawel")
    admin = create_user("admin", is_superuser=True)

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


def test_standard_user_update(clean_db):
    db = next(override_get_db())
    username = "pawel"
    user = create_user(username, "1234")
    new_data = {
        "password": "new password",
        "is_active": False,
        "is_superuser": True,
    }
    get_user = lambda: db.query(models.User).filter(models.User.username == username).first()

    # converting to dict to prevent from querying db after update, thus getting already updated data
    old_user_data = get_user().__dict__
    response = client.patch(
        f"/users/{username}", headers=auth_header(username), json=new_data
    )
    assert response.status_code == 200
    new_standard_user = get_user()

    # password can be changed by user
    assert old_user_data["password"] != new_standard_user.password
    # 'standard' user can only change password
    assert old_user_data["is_active"] == new_standard_user.is_active
    assert old_user_data["is_superuser"] == new_standard_user.is_superuser


def test_standard_user_update_unauthorized(clean_db):
    db = next(override_get_db())
    username = "pawel"
    user = create_user(username, "1234")
    new_data = {
        "password": "new password",
        "is_active": False,
        "is_superuser": True,
    }
    get_user = lambda: db.query(models.User).filter(models.User.username == username).first()

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
    db = next(override_get_db())
    username = "pawel"
    username_2 = "kamilek"
    user = create_user(username, "1234")
    user2 = create_user(username_2, "1234")
    new_data = {
        "password": "new password",
        "is_active": False,
        "is_superuser": True,
    }
    get_user = lambda: db.query(models.User).filter(models.User.username == username).first()

    # converting to dict to prevent from querying db after update, thus getting already updated data
    old_user_data = get_user().__dict__
    response = client.patch(
        f"/users/{username}", headers=auth_header(username_2), json=new_data
    )
    assert response.status_code == 401
    new_standard_user = get_user()
    # no changes
    assert old_user_data["password"] == new_standard_user.password
    assert old_user_data["is_active"] == new_standard_user.is_active
    assert old_user_data["is_superuser"] == new_standard_user.is_superuser


def test_superuser_update(clean_db):
    db = next(override_get_db())
    username = "pawel"
    user = create_user(username, "1234")
    superuser = create_user("admin", "1234", is_superuser=True)
    new_data = {
        "password": "new password",
        "is_active": False,
        "is_superuser": True,
    }
    get_user = lambda: db.query(models.User).filter(models.User.username == username).first()

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
    pawel = create_user("pawel", "1234")

    response = client.get("/users/pawel", headers=auth_header("pawel"))
    assert response.status_code == 200
    old_updated_at = datetime.datetime.fromisoformat(response.json().get("updated_at"))
    
    time.sleep(1)  # wait 1 second to show difference

    response = client.patch("/users/pawel", headers=auth_header("pawel"), json={"password": "123"})
    assert response.status_code == 200
    new_updated_at = datetime.datetime.fromisoformat(response.json().get("updated_at"))

    assert new_updated_at - old_updated_at > datetime.timedelta(seconds=1)
