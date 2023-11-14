from fastapi import APIRouter, Query
from selenium.webdriver.common.by import By

from config import get_browser, get_settings
from utils import scroll_to_bottom
from .methods import printify_difficulties, KataTrainer
from .models import (
    CodeWarsDifficulty,
    CodeWarsProgressAliases,
    CodeWarsProgressValue,
    ProgrammingLanguage,
)

router = APIRouter(prefix="/kata", tags=["kata"])


@router.post("/solve/{kata_id}", status_code=200)
async def solve_one_kata(
    kata_id: str,
    language: ProgrammingLanguage = Query(
        ProgrammingLanguage.python,
        title="Programming language",
        description="Language with which to solve the kata",
    ),
    should_reset_solution: bool = Query(
        False,
        title="Should reset solution?",
        description="Whether to reset the solution before solving the kata",
    ),
) -> bool:
    print(
        f"▶️ Solving kata..."
        f" | kata_id: {kata_id}"
        f" | language: {language.value}"
        f" | should_reset_solution: {should_reset_solution}"
    )
    kata_trainer = KataTrainer(kata_id=kata_id, language=language)
    kata_trainer.process_kata(should_reset_solution=should_reset_solution)
    print(f"✅ Kata solved: {kata_trainer.is_solved}")
    return kata_trainer.is_solved


@router.post("/solve", status_code=200)
async def solve_many_katas(
    language: ProgrammingLanguage = Query(
        ProgrammingLanguage.python,
        title="Programming language",
        description="Language with which to solve the kata",
    ),
    difficulties: list[CodeWarsDifficulty] = Query(
        [CodeWarsDifficulty.eight_kyu, CodeWarsDifficulty.seven_kyu],
        title="Difficulties",
        description="Difficulties of the kata",
    ),
    progress: CodeWarsProgressAliases = Query(
        CodeWarsProgressAliases.not_trained,
        title="Progress",
        description="Progress of the kata",
    ),
    should_reset_solution: bool = Query(
        False,
        title="Should reset solution?",
        description="Whether to reset the solution before solving the kata",
    ),
) -> list[bool]:
    print(
        f"▶️ Solving katas..."
        f" | language: {language.value}"
        f" | difficulties: {printify_difficulties(difficulties)}"
        f" | progress: {progress.value}"
        f" | should_reset_solution: {should_reset_solution}"
    )

    kata_ids = await get_kata_ids(
        language=language,
        difficulties=difficulties,
        progress=progress,
    )
    kata_results = []
    for index, kata_id in enumerate(kata_ids):
        print(f"Processing kata {index}/{len(kata_ids)} {kata_id}...")
        try:
            kata_results.append(
                await solve_one_kata(
                    kata_id=kata_id,
                    language=language,
                    should_reset_solution=should_reset_solution,
                )
            )
        except Exception as e:
            print(e)
            kata_results.append(False)

    kata_solved_number = sum(kata_results)
    print(f"✅ Kata solved: {kata_solved_number}/{len(kata_results)}")
    return kata_results


@router.get("", status_code=200)
async def get_kata_ids(
    language: ProgrammingLanguage = Query(
        ProgrammingLanguage.python,
        title="Programming language",
        description="Language with which to solve the kata",
    ),
    difficulties: list[CodeWarsDifficulty] = Query(
        [CodeWarsDifficulty.eight_kyu, CodeWarsDifficulty.seven_kyu],
        title="Difficulties",
        description="Difficulties of the kata",
    ),
    progress: CodeWarsProgressAliases = Query(
        CodeWarsProgressAliases.not_trained,
        title="Progress",
        description="Progress of the kata",
    ),
) -> list[str]:
    print(
        f"▶️ Getting kata ids..."
        f" | language: {language.value}"
        f" | difficulties: {printify_difficulties(difficulties)}"
        f" | progress: {progress.value}"
    )
    progress_value = CodeWarsProgressValue[progress]
    browser = get_browser()
    if progress_value in [
        CodeWarsProgressValue.unfinished,
        CodeWarsProgressValue.obsolete,
        CodeWarsProgressValue.completed,
    ]:
        browser.get(
            f"{get_settings().code_wars_url}/users/{get_settings().pseudo}/{progress.value}"
        )
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

    else:
        url = f"{get_settings().code_wars_url}/kata/search/{language.value}?q="
        for difficulty in difficulties:
            url += f"&r%5B%5D=-{difficulty.value}"
        url += f"&{progress_value.value}&beta=false&order_by=sort_date%20desc"

        browser.get(url)
        katas = browser.find_elements(By.CLASS_NAME, "list-item-kata")
        kata_ids = [kata.get_attribute("id") for kata in katas]

    print(f"✅ Kata ids found: {len(kata_ids)}")
    return kata_ids
