from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import get_settings, load_local_variables

load_local_variables()
from chains import solve_kata

from models import ProgrammingLanguage, CodeWarsDifficulty, CodeWarsProgress, TestButton


def login_code_wars(browser: webdriver.Remote):
    browser.get("https://www.codewars.com/users/sign_in")
    browser.find_element(By.ID, "user_email").send_keys(get_settings().email)
    browser.find_element(By.ID, "user_password").send_keys(get_settings().password)
    buttons = browser.find_elements(By.TAG_NAME, "button")
    buttons[-1].click()


def list_kata_ids(
    browser: webdriver.Remote,
    language: ProgrammingLanguage,
    difficulty: CodeWarsDifficulty,
    progress: CodeWarsProgress = CodeWarsProgress.not_trained,
) -> list[str]:
    browser.get(
        f"https://www.codewars.com/kata/search/{language.value}?q=&r%5B%5D=-{difficulty.value}&{progress.value}&beta=false&order_by=sort_date%20desc"
    )
    katas = browser.find_elements(By.CLASS_NAME, "list-item-kata")
    return [kata.get_attribute("id") for kata in katas]


class KataTraining:
    browser: webdriver.Remote

    TEST_TIMEOUT = 12
    PASSED_ALL_THE_TESTS = "You have passed all of the tests! :)"

    def __init__(
        self, browser: webdriver.Remote, kata_id: str, language: ProgrammingLanguage
    ):
        print(f"Processing kata {kata_id} for {language.value}...")
        self.browser = browser
        self.browser.get(
            f"https://www.codewars.com/kata/{kata_id}/train/{language.value}"
        )

    def send_solution(self, solution: str):
        code_tag = self.browser.find_element(By.ID, "code")
        textarea = code_tag.find_element(By.TAG_NAME, "textarea")
        # We delete the initial code
        textarea.send_keys(Keys.COMMAND, "a")
        textarea.send_keys(Keys.DELETE)

        # We send the solution
        textarea.send_keys(solution)

    def click_button_for_action(self, button_id: TestButton):
        self.browser.find_element(By.ID, button_id.value).click()
        print(f"{button_id.name.capitalize()}...")

    def find_solution(self) -> str:
        kata_description = self.browser.find_element(By.ID, "description").text
        print(
            f"""----------------
        Found the kata description: 
        {kata_description}"""
        )

        code_tag = self.browser.find_element(By.ID, "code")
        pre_code = code_tag.find_elements(By.TAG_NAME, "pre")
        initial_code = "\n".join([tag.text for tag in pre_code if tag.text])
        print(
            f"""----------------
        Found the initial code:
         {initial_code}"""
        )

        solution = solve_kata(
            kata_description=kata_description,
            programming_language=language,
            initial_code=initial_code,
        )
        print(
            f"""----------------
        Found the solution: 
        {solution}"""
        )
        return solution

    def are_tests_successful(self) -> bool:
        # TODO: Can sleep and check the results at the same time

        sleep(self.TEST_TIMEOUT)  # The tests timeout is 12 seconds

        iframe = self.browser.find_element(By.TAG_NAME, "iframe")
        self.browser.switch_to.frame(iframe)
        results = self.browser.find_element(By.CLASS_NAME, "run-results")
        success = self.PASSED_ALL_THE_TESTS in results.text.split("\n")
        self.browser.switch_to.default_content()
        return success

    def submit(self):
        self.browser.find_element(By.ID, "submit_btn").click()
        print("Submitting...")

    def process_kata(self):
        solution = self.find_solution()
        self.send_solution(solution=solution)
        self.click_button_for_action(button_id=TestButton.testing)

        if self.are_tests_successful():
            self.click_button_for_action(button_id=TestButton.attempting)
            if self.are_tests_successful():
                print("All checks passed!")
                self.click_button_for_action(button_id=TestButton.submitting)


if __name__ == "__main__":
    browser = webdriver.Firefox()
    language = ProgrammingLanguage.python
    difficulty = CodeWarsDifficulty.eight_kyu

    try:
        login_code_wars(browser)
        print("Logged in!")
        kata_ids = list_kata_ids(
            browser=browser,
            language=language,
            difficulty=difficulty,
        )
        print(f"{len(kata_ids)} katas found!")
        kata_training = KataTraining(
            browser=browser, kata_id=kata_ids[0], language=language
        )
        kata_training.process_kata()
    except Exception as e:
        print(e)

    sleep(15)
    browser.quit()
