from src.twitch.api.twitchEmoteImageFormat import TwitchEmoteImageFormat


class TestTwitchEmoteImageFormat():

    def test_fromStr_withAffiliateString(self):
        result = TwitchEmoteImageFormat.fromStr('animated')
        assert result is TwitchEmoteImageFormat.ANIMATED

    def test_fromStr_withEmptyString(self):
        result = TwitchEmoteImageFormat.fromStr('')
        assert result is TwitchEmoteImageFormat.DEFAULT

    def test_fromStr_withNone(self):
        result = TwitchEmoteImageFormat.fromStr(None)  # type: ignore
        assert result is TwitchEmoteImageFormat.DEFAULT

    def test_fromStr_withPartnerString(self):
        result = TwitchEmoteImageFormat.fromStr('static')
        assert result is TwitchEmoteImageFormat.STATIC

    def test_fromStr_withWhitespaceString(self):
        result = TwitchEmoteImageFormat.fromStr(' ')
        assert result is TwitchEmoteImageFormat.DEFAULT
