import pytest

from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport


class TestTwitchWebsocketTransport():

    def test_requireSessionId_withEmptyString(self):
        transport = TwitchWebsocketTransport(sessionId = '')
        sessionId: str | None = None

        with pytest.raises(Exception):
            sessionId = transport.requireSessionId()

        assert sessionId is None

    def test_requireSessionId_withNone(self):
        transport = TwitchWebsocketTransport()
        sessionId: str | None = None

        with pytest.raises(Exception):
            sessionId = transport.requireSessionId()

        assert sessionId is None

    def test_requireSessionId_withValidString(self):
        transport = TwitchWebsocketTransport(sessionId = 'abc123')
        assert transport.requireSessionId() == 'abc123'

    def test_requireSessionId_withWhitespaceString(self):
        transport = TwitchWebsocketTransport(sessionId = ' ')
        sessionId: str | None = None

        with pytest.raises(Exception):
            sessionId = transport.requireSessionId()

        assert sessionId is None
