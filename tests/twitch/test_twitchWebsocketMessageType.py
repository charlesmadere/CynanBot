from src.twitch.api.websocket.twitchWebsocketMessageType import \
    TwitchWebsocketMessageType


class TestTwitchWebsocketMessageType():

    def test_fromStr_withEmptyString(self):
        result = TwitchWebsocketMessageType.fromStr('')
        assert result is None

    def test_fromStr_withNone(self):
        result = TwitchWebsocketMessageType.fromStr(None)
        assert result is None

    def test_fromStr_withNotificationString(self):
        result = TwitchWebsocketMessageType.fromStr('notification')
        assert result is TwitchWebsocketMessageType.NOTIFICATION

    def test_fromStr_withRevocationString(self):
        result = TwitchWebsocketMessageType.fromStr('revocation')
        assert result is TwitchWebsocketMessageType.REVOCATION

    def test_fromStr_withSessionKeepAliveString(self):
        result = TwitchWebsocketMessageType.fromStr('session_keepalive')
        assert result is TwitchWebsocketMessageType.KEEP_ALIVE

    def test_fromStr_withSessionReconnectString(self):
        result = TwitchWebsocketMessageType.fromStr('session_reconnect')
        assert result is TwitchWebsocketMessageType.RECONNECT

    def test_fromStr_withSessionWelcomeString(self):
        result = TwitchWebsocketMessageType.fromStr('session_welcome')
        assert result is TwitchWebsocketMessageType.WELCOME

    def test_fromStr_withWhitespaceString(self):
        result = TwitchWebsocketMessageType.fromStr(' ')
        assert result is None
