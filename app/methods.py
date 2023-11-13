from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from config import get_settings

from models import ProgrammingLanguage, CodeWarsDifficulty, CodeWarsProgress


def login_code_wars(browser: webdriver.Remote):
    browser.get("https://www.codewars.com/users/sign_in")
    browser.find_element(By.ID, "user_email").send_keys(get_settings().email)
    browser.find_element(By.ID, "user_password").send_keys(get_settings().password)
    buttons = browser.find_elements(By.TAG_NAME, "button")
    buttons[-1].click()


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


def list_kata_ids(
    browser: webdriver.Remote,
    language: ProgrammingLanguage,
    difficulties: list[CodeWarsDifficulty],
    progress: CodeWarsProgress = CodeWarsProgress.not_trained,
) -> list[str]:
    if progress in [
        CodeWarsProgress.unfinished,
        CodeWarsProgress.obsolete,
        CodeWarsProgress.completed,
    ]:
        browser.get(f"https://www.codewars.com/users/grobec/{progress.value}")
        scroll_to_bottom(browser=browser)
        kata_list = browser.find_elements(By.CLASS_NAME, "list-item-solutions")
        kata_ids = []
        for kata in kata_list:
            kata_difficulty = kata.find_element(By.TAG_NAME, "span").text
            if kata_difficulty not in [
                f"{difficulty.value} kyu" for difficulty in difficulties
            ]:
                continue

            solution_languages = [
                solution_language.text.lower()
                for solution_language in kata.find_elements(By.TAG_NAME, "h6")
            ]
            if f"{language.value}:" not in solution_languages:
                continue

            title = kata.find_element(By.CLASS_NAME, "item-title")
            href = title.find_element(By.TAG_NAME, "a").get_attribute("href")
            kata_ids.append(href.split("/")[-1])

        return kata_ids

    else:
        url = f"https://www.codewars.com/kata/search/{language.value}?q="
        for difficulty in difficulties:
            url += f"&r%5B%5D=-{difficulty.value}"
        url += f"&{progress.value}&beta=false&order_by=sort_date%20desc"

        browser.get(url)
        katas = browser.find_elements(By.CLASS_NAME, "list-item-kata")
        return [kata.get_attribute("id") for kata in katas]
