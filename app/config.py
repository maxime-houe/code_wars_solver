from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "code_wars_gpt"
    version: str = "0.1.0"
    stage: str = "local"
    location: str = "local"
    environment: str = f"{stage}-{location}"

    email: str
    password: str


@lru_cache()
def get_settings():
    return Settings()
