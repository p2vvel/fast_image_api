from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from api import config

engine = create_engine(config.DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# DB dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
