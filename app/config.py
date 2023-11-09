import os


from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


def load_local_variables():
    # Load environment variables from local.env file
    load_dotenv("../local.env")
    load_dotenv("local.env")
    # Convert uppercase environment variables to lowercase
    for key, value in os.environ.items():
        if key.isupper():
            os.environ[key.lower()] = value


class Settings(BaseSettings):
    project_name: str = "code_wars_gpt"
    version: str = "0.1.0"
    stage: str = "local"
    location: str = "local"
    environment: str = f"{stage}-{location}"

    # Credentials CodeWars
    email: str
    password: str

    # OpenAI
    openai_api_key: str


@lru_cache()
def get_settings():
    return Settings()
