# from fastapi.testclient import TestClient
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine


# from api.main import app
# from api.database import get_db, Base



# engine = create_engine("sqlite:///./test_db.sqlite", connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()




# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)



# def test_users():
#     response = client.get("/users_temp")
#     assert response.status_code == 200
#     assert response.json() == []