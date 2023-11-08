from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from config import get_settings


def login_code_wars(browser: webdriver.Remote):
    browser.get("https://www.codewars.com/users/sign_in")
    browser.find_element(By.ID, "user_email").send_keys(get_settings().email)
    browser.find_element(By.ID, "user_password").send_keys(get_settings().password)
    buttons = browser.find_elements(By.TAG_NAME, "button")
    buttons[-1].click()


if __name__ == "__main__":
    browser = webdriver.Firefox()
    try:
        login_code_wars(browser)
    except Exception as e:
        print(e)

    sleep(15)
    browser.quit()
