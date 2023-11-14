from time import sleep

from selenium import webdriver
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
import tiktoken

from config import get_settings


# Define OpenAI Models
embedding = OpenAIEmbeddings(deployment="text-embedding-ada-002")
gpt_35 = ChatOpenAI(
    openai_api_key=get_settings().openai_api_key,
    model_name="gpt-3.5-turbo",
    temperature=0.4,
    streaming=True,
)
gpt_35_16k = ChatOpenAI(
    openai_api_key=get_settings().openai_api_key,
    model_name="gpt-3.5-turbo-16k",
    temperature=0.4,
    streaming=True,
)
gpt_4 = ChatOpenAI(
    openai_api_key=get_settings().openai_api_key,
    model_name="gpt-4",
    temperature=0,
    streaming=True,
)
ENCODING_NAME_FOR_GPT_MODELS = "cl100k_base"
GPT_35_MAXIMUM_CONTEST_TOKEN_LENGTH = 4097


def check_tokens_count_for_gpt_35(string: str) -> bool:
    encoding = tiktoken.get_encoding(ENCODING_NAME_FOR_GPT_MODELS)
    tokens_count = len(encoding.encode(string))
    return tokens_count < GPT_35_MAXIMUM_CONTEST_TOKEN_LENGTH


def is_at_bottom(browser: webdriver.Remote) -> bool:
    # Get the current scroll position
    current_scroll_position = browser.execute_script("return window.pageYOffset;")

    # Get the maximum scroll height of the page
    max_scroll_height = browser.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
    )
    current_window_height = browser.execute_script("return window.innerHeight;")
    print(f"Current scroll position: {current_scroll_position}")
    print(f"Max scroll height: {max_scroll_height}")
    print(f"Current window height: {current_window_height}")

    buffer = 10

    # Check if the current scroll position is equal to the maximum scroll height
    return current_scroll_position + current_window_height + buffer >= max_scroll_height


def scroll_to_bottom(browser: webdriver.Remote):
    # Scroll down to the bottom of the page
    while not is_at_bottom(browser=browser):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)  # Adjust the sleep time as needed
