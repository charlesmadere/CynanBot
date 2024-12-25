import pytest

from src.twitch.api.websocket.twitchWebsocketTransport import TwitchWebsocketTransport
from src.twitch.api.websocket.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


class TestTwitchWebsocketTransport:

    def test_requireSessionId_withEmptyString(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            conduitId = None,
            secret = None,
            sessionId = '',
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        sessionId: str | None = None

        with pytest.raises(Exception):
            sessionId = transport.requireSessionId()

        assert sessionId is None

    def test_requireSessionId_withNone(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            conduitId = None,
            secret = None,
            sessionId = None,
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        sessionId: str | None = None

        with pytest.raises(Exception):
            sessionId = transport.requireSessionId()

        assert sessionId is None

    def test_requireSessionId_withValidString(self):
        sessionId = 'abc123'

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            conduitId = None,
            secret = None,
            sessionId = sessionId,
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        assert transport.requireSessionId() == sessionId

    def test_requireSessionId_withWhitespaceString(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            conduitId = None,
            secret = None,
            sessionId = ' ',
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        sessionId: str | None = None

        with pytest.raises(Exception):
            sessionId = transport.requireSessionId()

        assert sessionId is None
