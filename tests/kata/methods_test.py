from pytest import mark


from kata.methods import printify_difficulties
from kata.models import CodeWarsDifficulty


class TestPrintifyDifficulties:
    @mark.unit
    @mark.parametrize(
        "difficulties, expected",
        [
            ([CodeWarsDifficulty.eight_kyu], "8"),
            ([CodeWarsDifficulty.eight_kyu, CodeWarsDifficulty.seven_kyu], "7, 8"),
            ([CodeWarsDifficulty.six_kyu, CodeWarsDifficulty.eight_kyu], "6, 8"),
        ],
    )
    def test_usual_case(self, difficulties, expected):
        assert printify_difficulties(difficulties) == expected
