import os
from enum import Enum

from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from selenium import webdriver


def load_local_variables():
    # Load environment variables from local.env file
    load_dotenv("../local.env")
    load_dotenv("local.env")
    # Convert uppercase environment variables to lowercase
    for key, value in os.environ.items():
        if key.isupper():
            os.environ[key.lower()] = value


load_local_variables()


class Settings(BaseSettings):
    project_name: str = "code_wars_gpt"
    version: str = "0.1.0"
    stage: str = "local"
    location: str = "local"
    environment: str = f"{stage}-{location}"
    code_wars_url: str = "https://www.codewars.com"

    # Credentials CodeWars
    email: str
    password: str
    pseudo: str

    # OpenAI
    openai_api_key: str


@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_browser() -> webdriver.Remote:
    return webdriver.Firefox()
