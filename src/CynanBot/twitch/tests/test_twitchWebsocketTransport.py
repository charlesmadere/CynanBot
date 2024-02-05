from typing import Optional

from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport


class TestTwitchWebsocketTransport():

    def test_requireSessionId_withEmptyString(self):
        transport = TwitchWebsocketTransport(sessionId = '')
        sessionId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            sessionId = transport.requireSessionId()
        except Exception as e:
            exception = e

        assert sessionId is None
        assert isinstance(exception, Exception)

    def test_requireSessionId_withNone(self):
        transport = TwitchWebsocketTransport()
        sessionId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            sessionId = transport.requireSessionId()
        except Exception as e:
            exception = e

        assert sessionId is None
        assert isinstance(exception, Exception)

    def test_requireSessionId_withValidString(self):
        transport = TwitchWebsocketTransport(sessionId = 'abc123')
        assert transport.requireSessionId() == 'abc123'

    def test_requireSessionId_withWhitespaceString(self):
        transport = TwitchWebsocketTransport(sessionId = ' ')
        sessionId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            sessionId = transport.requireSessionId()
        except Exception as e:
            exception = e

        assert sessionId is None
        assert isinstance(exception, Exception)
