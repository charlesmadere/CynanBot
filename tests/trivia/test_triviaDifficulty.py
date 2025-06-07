from src.trivia.triviaDifficulty import TriviaDifficulty


class TestTriviaDifficulty:

    def test_fromInt_withFour(self):
        result = TriviaDifficulty.fromInt(4)
        assert result is TriviaDifficulty.UNKNOWN

    def test_fromInt_withNegativeOne(self):
        result = TriviaDifficulty.fromInt(-1)
        assert result is TriviaDifficulty.UNKNOWN

    def test_fromInt_withNone(self):
        result = TriviaDifficulty.fromInt(None)
        assert result is TriviaDifficulty.UNKNOWN

    def test_fromInt_withOne(self):
        result = TriviaDifficulty.fromInt(1)
        assert result is TriviaDifficulty.EASY

    def test_fromInt_withThree(self):
        result = TriviaDifficulty.fromInt(3)
        assert result is TriviaDifficulty.HARD

    def test_fromInt_withTwo(self):
        result = TriviaDifficulty.fromInt(2)
        assert result is TriviaDifficulty.MEDIUM

    def test_fromInt_withZero(self):
        result = TriviaDifficulty.fromInt(0)
        assert result is TriviaDifficulty.UNKNOWN

    def test_fromStr_withEmptyString(self):
        result = TriviaDifficulty.fromStr('')
        assert result is TriviaDifficulty.UNKNOWN

    def test_fromStr_withEasyString(self):
        result = TriviaDifficulty.fromStr('easy')
        assert result is TriviaDifficulty.EASY

    def test_fromStr_withHardString(self):
        result = TriviaDifficulty.fromStr('hard')
        assert result is TriviaDifficulty.HARD

    def test_fromStr_withMediumString(self):
        result = TriviaDifficulty.fromStr('medium')
        assert result is TriviaDifficulty.MEDIUM

    def test_fromStr_withNone(self):
        result = TriviaDifficulty.fromStr(None)
        assert result is TriviaDifficulty.UNKNOWN

    def test_fromStr_withWhitespaceString(self):
        result = TriviaDifficulty.fromStr(' ')
        assert result is TriviaDifficulty.UNKNOWN

    def test_toInt(self):
        results: set[int] = set()

        for difficulty in TriviaDifficulty:
            results.add(difficulty.toInt())

        assert len(results) == len(TriviaDifficulty)

    def test_toInt_withEasy(self):
        result = TriviaDifficulty.EASY.toInt()
        assert result == 1

    def test_toInt_withHard(self):
        result = TriviaDifficulty.HARD.toInt()
        assert result == 3

    def test_toInt_withMedium(self):
        result = TriviaDifficulty.MEDIUM.toInt()
        assert result == 2

    def test_toInt_withUnknown(self):
        result = TriviaDifficulty.UNKNOWN.toInt()
        assert result == 0

    def test_toStr(self):
        results: set[str] = set()

        for difficulty in TriviaDifficulty:
            results.add(difficulty.toStr())

        assert len(results) == len(TriviaDifficulty)

    def test_toStr_withEasy(self):
        result = TriviaDifficulty.EASY.toStr()
        assert result == 'easy'

    def test_toStr_withHard(self):
        result = TriviaDifficulty.HARD.toStr()
        assert result == 'hard'

    def test_toStr_withMedium(self):
        result = TriviaDifficulty.MEDIUM.toStr()
        assert result == 'medium'

    def test_toStr_withUnkown(self):
        result = TriviaDifficulty.UNKNOWN.toStr()
        assert result == 'unknown'
