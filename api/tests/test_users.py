from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


from .utils import create_test_app


app = create_test_app()
client = TestClient(app)



def test_users():
    response = client.get("/auth/users")
    assert response.status_code == 401

    