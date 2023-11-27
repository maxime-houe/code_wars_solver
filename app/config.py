import os
from functools import lru_cache
import logging.config

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


__version__ = "0.1.1"


def configure_log():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        handlers=[
            logging.StreamHandler()  # Add a stream handler to log to the console
        ],
    )
    # # remove every other logger's handlers
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).setLevel(logging.WARNING)
        logging.getLogger(name).propagate = True


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
    version: str = __version__
    stage: str = "local"
    location: str = "local"
    environment: str = f"{stage}-{location}"
    code_wars_url: str = "https://www.codewars.com"
    headless_browser: str = "false"

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
    options = Options()
    if get_settings().headless_browser == "true":
        options.add_argument("--headless")
    return webdriver.Firefox(options=options)
