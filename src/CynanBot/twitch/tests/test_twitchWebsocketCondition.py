import pytest

from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition


class TestTwitchWebsocketCondition():

    def test_requireBroadcasterUserId_withEmptyString(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = ''
        )

        broadcasterUserId: str | None = None

        with pytest.raises(Exception):
            broadcasterUserId = condition.requireBroadcasterUserId()

        assert broadcasterUserId is None

    def test_requireBroadcasterUserId_withNone(self):
        condition = TwitchWebsocketCondition()
        broadcasterUserId: str | None = None

        with pytest.raises(Exception):
            broadcasterUserId = condition.requireBroadcasterUserId()

        assert broadcasterUserId is None

    def test_requireBroadcasterUserId_withValidString(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'abc123'
        )

        assert condition.requireBroadcasterUserId() == 'abc123'

    def test_requireBroadcasterUserId_withWhitespaceString(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = ' '
        )

        broadcasterUserId: str | None = None

        with pytest.raises(Exception):
            broadcasterUserId = condition.requireBroadcasterUserId()

        assert broadcasterUserId is None
