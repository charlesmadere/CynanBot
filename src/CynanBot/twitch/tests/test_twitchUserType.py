from twitch.twitchUserType import TwitchUserType


class TestTwitchUserType():

    def test_fromStr_withAdminString(self):
        result = TwitchUserType.fromStr('admin')
        assert result is TwitchUserType.ADMIN

    def test_fromStr_withEmptyString(self):
        result = TwitchUserType.fromStr('')
        assert result is TwitchUserType.NORMAL

    def test_fromStr_withGlobalModString(self):
        result = TwitchUserType.fromStr('global_mod')
        assert result is TwitchUserType.GLOBAL_MOD

    def test_fromStr_withNone(self):
        result = TwitchUserType.fromStr(None)
        assert result is TwitchUserType.NORMAL

    def test_fromStr_withStaffString(self):
        result = TwitchUserType.fromStr('staff')
        assert result is TwitchUserType.STAFF

    def test_fromStr_withWhitespaceString(self):
        result = TwitchUserType.fromStr(' ')
        assert result is TwitchUserType.NORMAL
