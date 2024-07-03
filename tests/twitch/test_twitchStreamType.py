from src.twitch.api.twitchStreamType import TwitchStreamType


class TestTwitchStreamType():

    def test_fromStr_withEmptyString(self):
        result = TwitchStreamType.fromStr('')
        assert result is TwitchStreamType.UNKNOWN

    def test_fromStr_withLiveString(self):
        result = TwitchStreamType.fromStr('live')
        assert result is TwitchStreamType.LIVE

    def test_fromStr_withNone(self):
        result = TwitchStreamType.fromStr(None)
        assert result is TwitchStreamType.UNKNOWN

    def test_fromStr_withWhitespaceString(self):
        result = TwitchStreamType.fromStr(' ')
        assert result is TwitchStreamType.UNKNOWN
