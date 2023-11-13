from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from chains import solve_kata_first_try, solve_kata_with_error_context
from models import ProgrammingLanguage, Button


class KataTrainer:
    browser: webdriver.Remote
    description: str
    language: ProgrammingLanguage
    kata_id: str

    TEST_TIMEOUT = 12
    PASSED_ALL_THE_TESTS = "You have passed all of the tests! :)"

    def __init__(
        self, browser: webdriver.Remote, kata_id: str, language: ProgrammingLanguage
    ):
        self.language = language
        self.kata_id = kata_id
        self.browser = browser
        self.browser.get(
            f"https://www.codewars.com/kata/{self.kata_id}/train/{self.language.value}"
        )
        self.description = self.browser.find_element(By.ID, "description").text

    #         print(
    #             f"""----------------
    # Found the kata description:
    # {self.description}"""
    #         )

    def send_solution(self, solution: str):
        code_tag = self.browser.find_element(By.ID, "code")
        textarea = code_tag.find_element(By.TAG_NAME, "textarea")
        # We delete the initial code
        textarea.send_keys(Keys.COMMAND, "a")
        textarea.send_keys(Keys.DELETE)

        # We send the solution
        textarea.send_keys(solution)

    def click_button_for_action(self, button_id: Button):
        self.browser.find_element(By.ID, button_id.value).click()
        print(f"{button_id.name.capitalize()}...")

    def parse_code(self) -> str:
        code_tag = self.browser.find_element(By.ID, "code")
        pre_code = code_tag.find_elements(By.TAG_NAME, "pre")
        code = "\n".join([tag.text for tag in pre_code if tag.text])
        #         print(
        #             f"""----------------
        # Found the code:
        # {code}"""
        #         )
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

        #         print(
        #             f"""----------------
        # Found the solution:
        # {solution}"""
        #         )
        return solution

    def are_tests_successful(self) -> bool:
        iframe = self.browser.find_element(By.TAG_NAME, "iframe")
        self.browser.switch_to.frame(iframe)
        success = None
        t = time()

        while success is None and time() - t < self.TEST_TIMEOUT:
            try:
                results = self.browser.find_element(By.CLASS_NAME, "run-results")
                success = self.PASSED_ALL_THE_TESTS in results.text.split("\n")
            except Exception as _:
                pass

        self.browser.switch_to.default_content()

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

        if self.are_tests_successful():
            self.click_button_for_action(button_id=Button.attempting)
            if self.are_tests_successful():
                print("All checks passed!")
                sleep(1)
                self.click_button_for_action(button_id=Button.submitting)
                print("Submitted!")
                return True

        return False

    def retrieve_errors(self) -> str:
        iframe = self.browser.find_element(By.TAG_NAME, "iframe")
        self.browser.switch_to.frame(iframe)
        results = self.browser.find_element(By.CLASS_NAME, "run-results")
        errors = results.text
        self.browser.switch_to.default_content()
        print(
            f"""----------------
Found the errors:
{errors}"""
        )
        return errors

    def retry(self) -> bool:
        errors = self.retrieve_errors()
        return self.solve_kata(errors=errors)

    def process_kata(self):
        success = self.solve_kata()
        if success:
            print(f"Kata {self.kata_id} solved at first try!")
        else:
            print(f"Kata {self.kata_id} not solved at first try!")
            success = self.retry()

            if success:
                print(f"Kata {self.kata_id} solved at second try!")
            else:
                print(f"Kata {self.kata_id} not solved at second try!")

            sleep(5)

    def reset_kata_solution(self):
        self.click_button_for_action(button_id=Button.resetting)
        confirm_element = self.browser.find_element(By.CLASS_NAME, "confirm")
        confirm_element.find_element(By.TAG_NAME, "a").click()
        sleep(1)
