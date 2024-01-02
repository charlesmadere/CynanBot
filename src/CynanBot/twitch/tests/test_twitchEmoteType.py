from typing import Optional

from CynanBot.twitch.api.twitchEmoteType import TwitchEmoteType


class TestTwitchEmoteType():

    def test_fromStr_withBitstierString(self):
        result = TwitchEmoteType.fromStr('bitstier')
        assert result is TwitchEmoteType.BITS

    def test_fromStr_withEmptyString(self):
        result: Optional[TwitchEmoteType] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchEmoteType.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withFollowerString(self):
        result = TwitchEmoteType.fromStr('follower')
        assert result is TwitchEmoteType.FOLLOWER

    def test_fromStr_withNone(self):
        result: Optional[TwitchEmoteType] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchEmoteType.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withWhitespaceString(self):
        result: Optional[TwitchEmoteType] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchEmoteType.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withSubscriptionsString(self):
        result = TwitchEmoteType.fromStr('subscriptions')
        assert result is TwitchEmoteType.SUBSCRIPTIONS
