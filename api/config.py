from pydantic import BaseSettings
# from functools import lru_cache


class SettingsStorage(BaseSettings):
    algorithm: str = "HS256"
    db_url: str = "sqlite:///./db.sqlite"
    file_storage: str = "./images/"
    jwt_timedelta_minutes: int = 15

    secret: str = "d9b17b791db4a785cfaf89a02f5eb3b4459670d74d68be3900ce88de50a33e68"
    test_db_url: str = "sqlite:///./test_db.sqlite"
    image_url: str = "/images"

    environment: str = "dev"    # "prod" for production, "dev" for development

    class Config:
        env_file = ".env"


# @lru_cache()
# def settings():
#     return SettingsStorage()


settings = SettingsStorage()
