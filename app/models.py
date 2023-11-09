from enum import Enum


class ProgrammingLanguage(str, Enum):
    python = "python"
    rust = "rust"


class CodeWarsProgress(str, Enum):
    not_completed = "xids=completed"
    not_trained = "xids=played"
    completed = "xids=not_completed"


class CodeWarsDifficulty(int, Enum):
    eight_kyu = 8
    seven_kyu = 7
    six_kyu = 6
    five_kyu = 5
    four_kyu = 4
    three_kyu = 3
    two_kyu = 2
    one_kyu = 1


class TestButton(str, Enum):
    testing = "validate_btn"
    attempting = "attempt_btn"
    submitting = "submit_btn"
