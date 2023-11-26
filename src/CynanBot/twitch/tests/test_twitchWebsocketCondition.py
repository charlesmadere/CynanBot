from typing import Optional

from twitch.websocket.websocketCondition import WebsocketCondition


class TestTwitchWebsocketCondition():

    def test_requireBroadcasterUserId_withEmptyString(self):
        condition = WebsocketCondition(
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
        condition = WebsocketCondition()
        broadcasterUserId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            broadcasterUserId = condition.requireBroadcasterUserId()
        except Exception as e:
            exception = e

        assert broadcasterUserId is None
        assert isinstance(exception, Exception)

    def test_requireBroadcasterUserId_withValidString(self):
        condition = WebsocketCondition(
            broadcasterUserId = 'abc123'
        )

        assert condition.requireBroadcasterUserId() == 'abc123'

    def test_requireBroadcasterUserId_withWhitespaceString(self):
        condition = WebsocketCondition(
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
