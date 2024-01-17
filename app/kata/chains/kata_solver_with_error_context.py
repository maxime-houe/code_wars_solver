from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from kata.models import ProgrammingLanguage
from utils import gpt_35

prompt_template = """You are a developer expert in solving kata (simple programming problem) on codewars.
You are receiving the description of a kata, the programming language, the previous code and the errors generated.
Your goal is to solve the problem by fixing the code provided. You have to change the provided code one way or another.

!!!IMPORTANT!!!
- YOU KEEP THE SAME FUNCTION OR CLASS AND PARAMETERS DEFINED IN THE PROVIDED CODE.
- YOUR RESPONSE SHOULD ONLY BE CODE. IF SOMEONE RUNS YOUR RESPONSE AS IS, IT SHOULD WORK.
- DO NOT ADD EXPLANATIONS.
- DO NOT ADD PRINTS FOR DEMONSTRATION OF YOUR SOLUTION.
- BE CAREFUL WITH " AND ' IN YOUR CODE.

input:
DESCRIPTION
{kata_description}
-------------------
PROGRAMMING LANGUAGE
{programming_language}
-----------------
CODE
{code}
-----------------
ERRORS
{errors}
"""
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["kata_description", "programming_language", "code", "errors"],
)

kata_solver_with_error_context = LLMChain(
    llm=gpt_35,
    prompt=prompt,
)


def solve_kata_with_error_context(
    kata_description: str,
    programming_language: ProgrammingLanguage,
    code: str,
    errors: str,
) -> str:
    generation = kata_solver_with_error_context.invoke(
        {
            "kata_description": kata_description,
            "programming_language": programming_language.value,
            "code": code,
            "errors": errors,
        }
    )
    return generation["text"]
