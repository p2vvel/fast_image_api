from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import config
from ..database import Base, get_db



def create_test_app():
    from ..main import app
    engine = create_engine(config.TEST_DB_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    return app
