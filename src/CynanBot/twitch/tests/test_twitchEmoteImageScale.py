from typing import Optional

from CynanBot.twitch.twitchEmoteImageScale import TwitchEmoteImageScale


class TestTwitchEmoteImageScale():

    def test_fromStr_withEmptyString(self):
        result: Optional[TwitchEmoteImageScale] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchEmoteImageScale.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withNone(self):
        result: Optional[TwitchEmoteImageScale] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchEmoteImageScale.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withWhitespaceString(self):
        result: Optional[TwitchEmoteImageScale] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchEmoteImageScale.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withUrl1xString(self):
        result = TwitchEmoteImageScale.fromStr('url_1x')
        assert result is TwitchEmoteImageScale.SMALL

    def test_fromStr_withUrl2xString(self):
        result = TwitchEmoteImageScale.fromStr('url_2x')
        assert result is TwitchEmoteImageScale.MEDIUM

    def test_fromStr_withUrl4xString(self):
        result = TwitchEmoteImageScale.fromStr('url_4x')
        assert result is TwitchEmoteImageScale.LARGE

    def test_fromStr_with10String(self):
        result = TwitchEmoteImageScale.fromStr('1.0')
        assert result is TwitchEmoteImageScale.SMALL

    def test_fromStr_with20String(self):
        result = TwitchEmoteImageScale.fromStr('2.0')
        assert result is TwitchEmoteImageScale.MEDIUM

    def test_fromStr_with30String(self):
        result = TwitchEmoteImageScale.fromStr('3.0')
        assert result is TwitchEmoteImageScale.LARGE
