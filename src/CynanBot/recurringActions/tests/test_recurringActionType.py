from typing import Optional

from CynanBot.recurringActions.recurringActionType import RecurringActionType


class TestRecurringActionType():

    def test_fromStr_withEmptyString(self):
        result: Optional[RecurringActionType] = None
        exception: Optional[Exception] = None

        try:
            result = RecurringActionType.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withNone(self):
        result: Optional[RecurringActionType] = None
        exception: Optional[Exception] = None

        try:
            result = RecurringActionType.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withSuperTriviaStrings(self):
        result = RecurringActionType.fromStr('supertrivia')
        assert result is RecurringActionType.SUPER_TRIVIA

        result = RecurringActionType.fromStr('super_trivia')
        assert result is RecurringActionType.SUPER_TRIVIA

    def test_fromStr_withSuperTrivia_toStr(self):
        string = RecurringActionType.SUPER_TRIVIA.toStr()
        result = RecurringActionType.fromStr(string)
        assert result is RecurringActionType.SUPER_TRIVIA

    def test_fromStr_withWeatherString(self):
        result = RecurringActionType.fromStr('weather')
        assert result is RecurringActionType.WEATHER

    def test_fromStr_withWeather_toStr(self):
        string = RecurringActionType.WEATHER.toStr()
        result = RecurringActionType.fromStr(string)
        assert result is RecurringActionType.WEATHER

    def test_fromStr_withWordOfTheDayStrings(self):
        result = RecurringActionType.fromStr('word')
        assert result is RecurringActionType.WORD_OF_THE_DAY

        result = RecurringActionType.fromStr('wordoftheday')
        assert result is RecurringActionType.WORD_OF_THE_DAY

        result = RecurringActionType.fromStr('word_of_the_day')
        assert result is RecurringActionType.WORD_OF_THE_DAY

        result = RecurringActionType.fromStr('wotd')
        assert result is RecurringActionType.WORD_OF_THE_DAY

    def test_fromStr_withWordOfTheDay_toStr(self):
        string = RecurringActionType.WORD_OF_THE_DAY.toStr()
        result = RecurringActionType.fromStr(string)
        assert result is RecurringActionType.WORD_OF_THE_DAY

    def test_fromStr_withWhitespaceString(self):
        result: Optional[RecurringActionType] = None
        exception: Optional[Exception] = None

        try:
            result = RecurringActionType.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_toReadableStr_withWeather(self):
        result = RecurringActionType.SUPER_TRIVIA.toReadableStr()
        assert result == 'Super Trivia'

    def test_toReadableStr_withWeather(self):
        result = RecurringActionType.WEATHER.toReadableStr()
        assert result == 'Weather'

    def test_toReadableStr_withWordOfTheDay(self):
        result = RecurringActionType.WORD_OF_THE_DAY.toReadableStr()
        assert result == 'Word of the Day'

    def test_toStr_withWeather(self):
        result = RecurringActionType.SUPER_TRIVIA.toStr()
        assert result == 'super_trivia'

    def test_toStr_withWeather(self):
        result = RecurringActionType.WEATHER.toStr()
        assert result == 'weather'

    def test_toStr_withWordOfTheDay(self):
        result = RecurringActionType.WORD_OF_THE_DAY.toStr()
        assert result == 'word_of_the_day'
