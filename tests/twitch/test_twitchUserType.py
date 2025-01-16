from src.twitch.api.models.twitchUserType import TwitchUserType


class TestTwitchUserType:

    def test_toStr_withAdmin(self):
        result = TwitchUserType.ADMIN.toStr()
        assert result == 'admin'

    def test_toStr_withGlobalMod(self):
        result = TwitchUserType.GLOBAL_MOD.toStr()
        assert result == 'global_mod'

    def test_toStr_withNormal(self):
        result = TwitchUserType.NORMAL.toStr()
        assert result == 'normal'

    def test_toStr_withStaff(self):
        result = TwitchUserType.STAFF.toStr()
        assert result == 'staff'
