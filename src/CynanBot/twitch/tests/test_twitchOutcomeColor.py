from typing import Optional

from CynanBot.twitch.api.twitchOutcomeColor import TwitchOutcomeColor


class TestTwitchOutcomeColor():

    def test_fromStr_withBlueString(self):
        result = TwitchOutcomeColor.fromStr('blue')
        assert result is TwitchOutcomeColor.BLUE

    def test_fromStr_withEmptyString(self):
        result: Optional[TwitchOutcomeColor] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchOutcomeColor.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withNone(self):
        result: Optional[TwitchOutcomeColor] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchOutcomeColor.fromStr(None)  # type: ignore
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withPinkString(self):
        result = TwitchOutcomeColor.fromStr('pink')
        assert result is TwitchOutcomeColor.PINK

    def test_fromStr_withWhitespaceString(self):
        result: Optional[TwitchOutcomeColor] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchOutcomeColor.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)
