import pytest

from src.twitch.api.models.twitchWebsocketTransport import TwitchWebsocketTransport
from src.twitch.api.models.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


class TestTwitchWebsocketTransport:

    def test_requireCallbackUrl(self):
        callbackUrl = 'https://www.twitch.tv/'

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = callbackUrl,
            conduitId = None,
            secret = 'def456',
            sessionId = None,
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
        )

        assert transport.requireCallbackUrl() == callbackUrl

    def test_requireConduitId(self):
        conduitId = 'xyz789'

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = conduitId,
            secret = None,
            sessionId = None,
            method = TwitchWebsocketTransportMethod.CONDUIT,
        )

        assert transport.requireConduitId() == conduitId

    def test_requireSessionId(self):
        sessionId = 'abc123'

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = None,
            secret = None,
            sessionId = sessionId,
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
        )

        assert transport.requireSessionId() == sessionId

    def test_requireSessionId_withEmptyString(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = None,
            secret = None,
            sessionId = '',
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
        )

        sessionId: str | None = None

        with pytest.raises(ValueError):
            sessionId = transport.requireSessionId()

        assert sessionId is None

    def test_requireSessionId_withNone(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = None,
            secret = None,
            sessionId = None,
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
        )

        sessionId: str | None = None

        with pytest.raises(ValueError):
            sessionId = transport.requireSessionId()

        assert sessionId is None

    def test_requireSessionId_withWhitespaceString(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = None,
            secret = None,
            sessionId = ' ',
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
        )

        sessionId: str | None = None

        with pytest.raises(ValueError):
            sessionId = transport.requireSessionId()

        assert sessionId is None
