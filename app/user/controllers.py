from fastapi import APIRouter
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from config import get_browser, get_settings

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/login", status_code=200)
async def login():
    browser = get_browser()
    browser.get(f"{get_settings().code_wars_url}/users/sign_in")
    browser.find_element(By.ID, "user_email").send_keys(get_settings().email)
    browser.find_element(By.ID, "user_password").send_keys(get_settings().password)
    buttons = browser.find_elements(By.TAG_NAME, "button")
    buttons[-1].click()
    print("Logged in!")
    return {"status": "Logged in!"}


@router.get("/logout", status_code=200)
async def logout():
    browser = get_browser()
    browser.get(f"{get_settings().code_wars_url}")
    profile = browser.find_element(By.CLASS_NAME, "profile-item")
    actions = ActionChains(browser)
    actions.move_to_element(profile).perform()
    browser.find_element(By.CLASS_NAME, "js-sign-out").click()
    return {"status": "Logged out!"}
