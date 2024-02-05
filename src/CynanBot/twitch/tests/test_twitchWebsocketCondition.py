from typing import Optional

from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition


class TestTwitchWebsocketCondition():

    def test_requireBroadcasterUserId_withEmptyString(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = ''
        )

        broadcasterUserId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            broadcasterUserId = condition.requireBroadcasterUserId()
        except Exception as e:
            exception = e

        assert broadcasterUserId is None
        assert isinstance(exception, Exception)

    def test_requireBroadcasterUserId_withNone(self):
        condition = TwitchWebsocketCondition()
        broadcasterUserId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            broadcasterUserId = condition.requireBroadcasterUserId()
        except Exception as e:
            exception = e

        assert broadcasterUserId is None
        assert isinstance(exception, Exception)

    def test_requireBroadcasterUserId_withValidString(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'abc123'
        )

        assert condition.requireBroadcasterUserId() == 'abc123'

    def test_requireBroadcasterUserId_withWhitespaceString(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = ' '
        )

        broadcasterUserId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            broadcasterUserId = condition.requireBroadcasterUserId()
        except Exception as e:
            exception = e

        assert broadcasterUserId is None
        assert isinstance(exception, Exception)
