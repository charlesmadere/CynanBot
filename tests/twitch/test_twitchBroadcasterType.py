from src.twitch.api.twitchBroadcasterType import TwitchBroadcasterType


class TestTwitchBroadcasterType():

    def test_fromStr_withAffiliateString(self):
        result = TwitchBroadcasterType.fromStr('affiliate')
        assert result is TwitchBroadcasterType.AFFILIATE

    def test_fromStr_withEmptyString(self):
        result = TwitchBroadcasterType.fromStr('')
        assert result is TwitchBroadcasterType.NORMAL

    def test_fromStr_withNone(self):
        result = TwitchBroadcasterType.fromStr(None)
        assert result is TwitchBroadcasterType.NORMAL

    def test_fromStr_withPartnerString(self):
        result = TwitchBroadcasterType.fromStr('partner')
        assert result is TwitchBroadcasterType.PARTNER

    def test_fromStr_withWhitespaceString(self):
        result = TwitchBroadcasterType.fromStr(' ')
        assert result is TwitchBroadcasterType.NORMAL
