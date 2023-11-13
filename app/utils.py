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
