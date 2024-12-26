from src.twitch.api.models.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus


class TestTwitchWebsocketConnectionStatus:

    def test_fromStr_withAdminString(self):
        result = TwitchWebsocketConnectionStatus.fromStr('connected')
        assert result is TwitchWebsocketConnectionStatus.CONNECTED

    def test_fromStr_withAuthorizationRevokedString(self):
        result = TwitchWebsocketConnectionStatus.fromStr('authorization_revoked')
        assert result is TwitchWebsocketConnectionStatus.REVOKED

    def test_fromStr_withEmptyString(self):
        result = TwitchWebsocketConnectionStatus.fromStr('')
        assert result is None

    def test_fromStr_withEnabledString(self):
        result = TwitchWebsocketConnectionStatus.fromStr('enabled')
        assert result is TwitchWebsocketConnectionStatus.ENABLED

    def test_fromStr_withNone(self):
        result = TwitchWebsocketConnectionStatus.fromStr(None)
        assert result is None

    def test_fromStr_withReconnectingString(self):
        result = TwitchWebsocketConnectionStatus.fromStr('reconnecting')
        assert result is TwitchWebsocketConnectionStatus.RECONNECTING

    def test_fromStr_withUserRemovedString(self):
        result = TwitchWebsocketConnectionStatus.fromStr('user_removed')
        assert result is TwitchWebsocketConnectionStatus.USER_REMOVED

    def test_fromStr_withVersionRemovedString(self):
        result = TwitchWebsocketConnectionStatus.fromStr('version_removed')
        assert result is TwitchWebsocketConnectionStatus.VERSION_REMOVED

    def test_fromStr_withWhitespaceString(self):
        result = TwitchWebsocketConnectionStatus.fromStr(' ')
        assert result is None
