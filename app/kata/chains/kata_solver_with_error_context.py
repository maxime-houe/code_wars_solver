from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from kata.models import ProgrammingLanguage
from utils import gpt_35

prompt_template = """
You are a developer expert in solving kata (simple programming problem) on Codewars.
You are receiving the description of a kata, the programming language, the previous code and the errors generated.
Your goal is to solve the problem by fixing the code provided. You have to change the provided code one way or another.

**Important Instructions**:
- Keep the same function or class and parameters defined in the provided code.
- Your response should only be code. If someone runs your response as is, it should work.
- Do not add explanations or print statements for demonstration of your solution.
- Be careful with the usage of double quotes (") and single quotes (') in your code. Ensure they are used correctly to avoid syntax errors.

**Input**:
- Description: {kata_description}
- Programming Language: {programming_language}
- Code: {code}
- Errors: {errors}
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
    """
    Function to solve a kata using the GPT-3 model.

    Parameters:
    kata_description (str): The description of the kata.
    programming_language (ProgrammingLanguage): The programming language of the kata.
    code (str): The initial code of the kata.
    errors (str): The errors generated from the initial code.

    Returns:
    str: The generated solution for the kata.
    """
    try:
        generation = kata_solver_with_error_context.invoke(
            {
                "kata_description": kata_description,
                "programming_language": programming_language.value,
                "code": code,
                "errors": errors,
            }
        )
        return generation["text"]
    except Exception as e:
        print(f"An error occurred while solving the kata: {e}")
        return None
