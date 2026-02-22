from typing import Final

from src.websocketConnection.mapper.websocketEventTypeMapper import WebsocketEventTypeMapper
from src.websocketConnection.mapper.websocketEventTypeMapperInterface import WebsocketEventTypeMapperInterface
from src.websocketConnection.websocketEventType import WebsocketEventType


class TestWebsocketEventTypeMapper:

    mapper: Final[WebsocketEventTypeMapperInterface] = WebsocketEventTypeMapper()

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, WebsocketEventTypeMapper)
        assert isinstance(self.mapper, WebsocketEventTypeMapperInterface)

    def test_serializeEventType_withAll(self):
        results: set[str] = set()

        for eventType in WebsocketEventType:
            result = self.mapper.serializeEventType(eventType)
            results.add(result)

        assert len(results) == len(WebsocketEventType)

    def test_serializeEventType_withChannelPrediction(self):
        result = self.mapper.serializeEventType(WebsocketEventType.CHANNEL_PREDICTION)
        assert result == 'channelPrediction'

    def test_serializeEventType_withMouseCursor(self):
        result = self.mapper.serializeEventType(WebsocketEventType.MOUSE_CURSOR)
        assert result == 'mouseCursor'
