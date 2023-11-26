from CynanBot.twitch.websocket.websocketConnectionStatus import \
    WebsocketConnectionStatus


class TestTwitchWebsocketConnectionStatus():

    def test_fromStr_withAdminString(self):
        result = WebsocketConnectionStatus.fromStr('connected')
        assert result is WebsocketConnectionStatus.CONNECTED

    def test_fromStr_withAuthorizationRevokedString(self):
        result = WebsocketConnectionStatus.fromStr('authorization_revoked')
        assert result is WebsocketConnectionStatus.REVOKED

    def test_fromStr_withEmptyString(self):
        result = WebsocketConnectionStatus.fromStr('')
        assert result is None

    def test_fromStr_withEnabledString(self):
        result = WebsocketConnectionStatus.fromStr('enabled')
        assert result is WebsocketConnectionStatus.ENABLED

    def test_fromStr_withNone(self):
        result = WebsocketConnectionStatus.fromStr(None)
        assert result is None

    def test_fromStr_withReconnectingString(self):
        result = WebsocketConnectionStatus.fromStr('reconnecting')
        assert result is WebsocketConnectionStatus.RECONNECTING

    def test_fromStr_withUserRemovedString(self):
        result = WebsocketConnectionStatus.fromStr('user_removed')
        assert result is WebsocketConnectionStatus.USER_REMOVED

    def test_fromStr_withVersionRemovedString(self):
        result = WebsocketConnectionStatus.fromStr('version_removed')
        assert result is WebsocketConnectionStatus.VERSION_REMOVED

    def test_fromStr_withWhitespaceString(self):
        result = WebsocketConnectionStatus.fromStr(' ')
        assert result is None
