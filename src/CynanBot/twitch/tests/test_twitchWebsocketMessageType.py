from twitch.websocket.websocketMessageType import WebsocketMessageType


class TestTwitchWebsocketMessageType():

    def test_fromStr_withEmptyString(self):
        result = WebsocketMessageType.fromStr('')
        assert result is None

    def test_fromStr_withNone(self):
        result = WebsocketMessageType.fromStr(None)
        assert result is None

    def test_fromStr_withNotificationString(self):
        result = WebsocketMessageType.fromStr('notification')
        assert result is WebsocketMessageType.NOTIFICATION

    def test_fromStr_withRevocationString(self):
        result = WebsocketMessageType.fromStr('revocation')
        assert result is WebsocketMessageType.REVOCATION

    def test_fromStr_withSessionKeepAliveString(self):
        result = WebsocketMessageType.fromStr('session_keepalive')
        assert result is WebsocketMessageType.KEEP_ALIVE

    def test_fromStr_withSessionReconnectString(self):
        result = WebsocketMessageType.fromStr('session_reconnect')
        assert result is WebsocketMessageType.RECONNECT

    def test_fromStr_withSessionWelcomeString(self):
        result = WebsocketMessageType.fromStr('session_welcome')
        assert result is WebsocketMessageType.WELCOME

    def test_fromStr_withWhitespaceString(self):
        result = WebsocketMessageType.fromStr(' ')
        assert result is None
