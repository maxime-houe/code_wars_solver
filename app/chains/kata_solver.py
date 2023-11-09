from langchain import LLMChain, PromptTemplate

from models import ProgrammingLanguage
from utils import gpt_35

prompt_template = """You are a developer expert in solving kata (simple programming problem) on codewars.
You are receiving the description of a kata, the programming language and the initial code.
Your goal is to solve the problem by returning the initial code completed.

!!!IMPORTANT!!!
- YOUR RESPONSE SHOULD ONLY BE WORKING CODE.
- YOU CAN ADD EXPLANATIONS, BUT ONLY IN CODE COMMENTS.

input:
DESCRIPTION
{kata_description}
-------------------
PROGRAMMING LANGUAGE
{programming_language}
-----------------
INITIAL CODE
{initial_code}
"""
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["positive_traits", "negative_trait", "language"],
)

horoscope_chain = LLMChain(
    llm=gpt_35,
    prompt=prompt,
)


def solve_kata(
    kata_description: str,
    programming_language: ProgrammingLanguage,
    initial_code: str,
) -> str:
    generation = horoscope_chain(
        {
            "kata_description": kata_description,
            "programming_language": programming_language,
            "initial_code": initial_code,
        }
    )
    return generation["text"]
