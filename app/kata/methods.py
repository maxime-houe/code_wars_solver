from time import sleep, time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .chains import solve_kata_first_try, solve_kata_with_error_context
from config import get_settings, get_browser
from .models import ProgrammingLanguage, Button, CodeWarsDifficulty


def printify_difficulties(difficulties: list[CodeWarsDifficulty]) -> str:
    return ", ".join(sorted([str(difficulty.value) for difficulty in difficulties]))


class KataTrainer:
    description: str
    language: ProgrammingLanguage
    kata_id: str
    solution: str
    is_solved: bool = None

    TEST_TIMEOUT = 12
    PASSED_ALL_THE_TESTS = "You have passed all of the tests! :)"

    def __init__(self, kata_id: str, language: ProgrammingLanguage):
        self.language = language
        self.kata_id = kata_id
        get_browser().get(
            f"{get_settings().code_wars_url}/kata/{self.kata_id}/train/{self.language.value}"
        )
        self.description = get_browser().find_element(By.ID, "description").text

        logging.debug(
            f"""----------------
Found the kata description:
{self.description}"""
        )

    @staticmethod
    def send_solution(solution: str):
        code_tag = get_browser().find_element(By.ID, "code")
        textarea = code_tag.find_element(By.TAG_NAME, "textarea")
        # We delete the initial code
        textarea.send_keys(Keys.COMMAND, "a")
        textarea.send_keys(Keys.DELETE)

        # We send the solution
        textarea.send_keys(solution)

    @staticmethod
    def click_button_for_action(button_id: Button):
        get_browser().find_element(By.ID, button_id.value).click()
        logging.info(f"{button_id.name.capitalize()}...")

    @staticmethod
    def parse_code() -> str:
        code_tag = get_browser().find_element(By.ID, "code")
        pre_code = code_tag.find_elements(By.TAG_NAME, "pre")
        code = "\n".join([tag.text for tag in pre_code if tag.text])
        logging.debug(
            f"""----------------
Found the code:
{code}"""
        )
        return code

    def find_solution(self, errors: str) -> str:
        code = self.parse_code()

        if errors:
            solution = solve_kata_with_error_context(
                kata_description=self.description,
                programming_language=self.language,
                code=code,
                errors=errors,
            )

        else:
            solution = solve_kata_first_try(
                kata_description=self.description,
                programming_language=self.language,
                code=code,
            )

        logging.debug(
            f"""----------------
Found the solution:
{solution}"""
        )
        self.solution = solution
        return solution

    def are_tests_successful(self) -> bool:
        iframe = get_browser().find_element(By.TAG_NAME, "iframe")
        get_browser().switch_to.frame(iframe)
        success = None
        t = time()

        while success is None and time() - t < self.TEST_TIMEOUT:
            try:
                results = get_browser().find_element(By.CLASS_NAME, "run-results")
                success = self.PASSED_ALL_THE_TESTS in results.text.split("\n")
            except Exception as _:
                pass

        get_browser().switch_to.default_content()

        if success is None:
            success = False

        return success

    def solve_kata(self, errors: str = None) -> bool:
        """
        Solves a kata, return True if the kata was solved, False otherwise
        """
        solution = self.find_solution(errors=errors)
        self.send_solution(solution=solution)
        self.click_button_for_action(button_id=Button.testing)
        self.is_solved = False

        if self.are_tests_successful():
            self.click_button_for_action(button_id=Button.attempting)
            if self.are_tests_successful():
                logging.info("All checks passed!")
                sleep(1)
                self.click_button_for_action(button_id=Button.submitting)
                logging.info("Submitted!")
                self.is_solved = True

        return self.is_solved

    @staticmethod
    def retrieve_errors() -> str:
        iframe = get_browser().find_element(By.TAG_NAME, "iframe")
        get_browser().switch_to.frame(iframe)
        results = get_browser().find_element(By.CLASS_NAME, "run-results")
        errors = results.text
        get_browser().switch_to.default_content()
        logging.debug(
            f"""----------------
Found the errors:
{errors}"""
        )
        return errors

    def retry(self) -> bool:
        errors = self.retrieve_errors()
        return self.solve_kata(errors=errors)

    def process_kata(self, should_reset_solution: bool):
        if should_reset_solution:
            self.reset_kata_solution()

        success = self.solve_kata()
        if success:
            logging.info(f"Kata {self.kata_id} solved at first try!")
        else:
            logging.info(f"Kata {self.kata_id} not solved at first try!")
            success = self.retry()

            if success:
                logging.info(f"Kata {self.kata_id} solved at second try!")
            else:
                logging.info(f"Kata {self.kata_id} not solved at second try!")

            sleep(5)

    def reset_kata_solution(self):
        sleep(1)
        self.click_button_for_action(button_id=Button.resetting)
        confirm_element = get_browser().find_element(By.CLASS_NAME, "confirm")
        confirm_element.find_element(By.TAG_NAME, "a").click()
        sleep(1)
