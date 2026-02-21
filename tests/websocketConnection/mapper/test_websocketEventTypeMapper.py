from typing import Final

from src.websocketConnection.mapper.websocketEventTypeMapper import WebsocketEventTypeMapper
from src.websocketConnection.mapper.websocketEventTypeMapperInterface import WebsocketEventTypeMapperInterface
from src.websocketConnection.websocketEventType import WebsocketEventType


class TestWebsocketEventTypeMapper:

    mapper: Final[WebsocketEventTypeMapperInterface] = WebsocketEventTypeMapper()

    def test_toString_withAll(self):
        results: set[str] = set()

        for eventType in WebsocketEventType:
            result = self.mapper.toString(eventType)
            results.add(result)

        assert len(results) == len(WebsocketEventType)

    def test_toString_withChannelPrediction(self):
        result = self.mapper.toString(WebsocketEventType.CHANNEL_PREDICTION)
        assert result == 'channelPrediction'

    def test_toString_withMouseCursor(self):
        result = self.mapper.toString(WebsocketEventType.MOUSE_CURSOR)
        assert result == 'mouseCursor'
