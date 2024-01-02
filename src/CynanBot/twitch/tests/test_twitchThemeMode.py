from typing import Optional

from CynanBot.twitch.api.twitchThemeMode import TwitchThemeMode


class TestTwitchThemeMode():

    def test_fromStr_withEmptyString(self):
        result: Optional[TwitchThemeMode] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchThemeMode.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withDarkString(self):
        result = TwitchThemeMode.fromStr('dark')
        assert result is TwitchThemeMode.DARK

    def test_fromStr_withLightString(self):
        result = TwitchThemeMode.fromStr('light')
        assert result is TwitchThemeMode.LIGHT

    def test_fromStr_withNone(self):
        result: Optional[TwitchThemeMode] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchThemeMode.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withWhitespaceString(self):
        result: Optional[TwitchThemeMode] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchThemeMode.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)
