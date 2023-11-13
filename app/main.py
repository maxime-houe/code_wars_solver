from time import sleep

from selenium import webdriver

from config import load_local_variables

load_local_variables()


if __name__ == "__main__":
    from kata_trainer import KataTrainer
    from methods import list_kata_ids, login_code_wars
    from models import ProgrammingLanguage, CodeWarsDifficulty, CodeWarsProgress

    browser = webdriver.Firefox()
    language = ProgrammingLanguage.python
    difficulties = [CodeWarsDifficulty.eight_kyu, CodeWarsDifficulty.seven_kyu]

    login_code_wars(browser)
    print("Logged in!")
    kata_ids = list_kata_ids(
        browser=browser,
        language=language,
        difficulties=difficulties,
        progress=CodeWarsProgress.not_trained,
    )
    print(f"{len(kata_ids)} katas found!")
    for index, kata_id in enumerate(kata_ids):
        try:
            print(
                f"Processing kata {index}/{len(kata_ids)} {kata_id} for {language.value}..."
            )
            kata_trainer = KataTrainer(
                browser=browser, kata_id=kata_id, language=language
            )
            # kata_trainer.reset_kata_solution()
            kata_trainer.process_kata()
        except Exception as e:
            print(e)

        sleep(1)

    sleep(30)
    browser.quit()
