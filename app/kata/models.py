from enum import Enum


class ProgrammingLanguage(str, Enum):
    python = "python"
    rust = "rust"
    javascript = "javascript"


class CodeWarsProgressValue(str, Enum):
    not_completed = "xids=completed"
    not_trained = "xids=played"
    completed = "completed_solutions"
    unfinished = "unfinished_solutions"
    obsolete = "obsolete_solutions"


class CodeWarsProgressAliases(str, Enum):
    not_completed = "not_completed"
    not_trained = "not_trained"
    completed = "completed"
    unfinished = "unfinished"
    obsolete = "obsolete"


class CodeWarsDifficulty(int, Enum):
    eight_kyu = 8
    seven_kyu = 7
    six_kyu = 6
    five_kyu = 5
    four_kyu = 4
    three_kyu = 3
    two_kyu = 2
    one_kyu = 1


class Button(str, Enum):
    testing = "validate_btn"
    attempting = "attempt_btn"
    submitting = "submit_btn"
    resetting = "reset_btn"
