from src.websocketConnection.mapper.websocketEventTypeMapper import WebsocketEventTypeMapper
from src.websocketConnection.mapper.websocketEventTypeMapperInterface import WebsocketEventTypeMapperInterface
from src.websocketConnection.websocketEventType import WebsocketEventType


class TestWebsocketEventTypeMapper:

    mapper: WebsocketEventTypeMapperInterface = WebsocketEventTypeMapper()

    def test_toString_withChannelPrediction(self):
        result = self.mapper.toString(WebsocketEventType.CHANNEL_PREDICTION)
        assert result == 'channelPrediction'
