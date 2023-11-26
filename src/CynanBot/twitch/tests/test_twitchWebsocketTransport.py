from typing import Optional

from CynanBot.twitch.websocket.websocketTransport import WebsocketTransport


class TestTwitchWebsocketTransport():

    def test_requireSessionId_withEmptyString(self):
        transport = WebsocketTransport(sessionId = '')
        sessionId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            sessionId = transport.requireSessionId()
        except Exception as e:
            exception = e

        assert sessionId is None
        assert isinstance(exception, Exception)

    def test_requireSessionId_withNone(self):
        transport = WebsocketTransport()
        sessionId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            sessionId = transport.requireSessionId()
        except Exception as e:
            exception = e

        assert sessionId is None
        assert isinstance(exception, Exception)

    def test_requireSessionId_withValidString(self):
        transport = WebsocketTransport(sessionId = 'abc123')
        assert transport.requireSessionId() == 'abc123'

    def test_requireSessionId_withWhitespaceString(self):
        transport = WebsocketTransport(sessionId = ' ')
        sessionId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            sessionId = transport.requireSessionId()
        except Exception as e:
            exception = e

        assert sessionId is None
        assert isinstance(exception, Exception)
