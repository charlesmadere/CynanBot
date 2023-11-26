from typing import Optional

from CynanBot.twitch.websocket.websocketTransportMethod import \
    WebsocketTransportMethod


class TestTwitchWebsocketTransportMethod():

    def test_fromStr_withEmptyString(self):
        result: Optional[WebsocketTransportMethod] = None
        exception: Optional[Exception] = None

        try:
            result = WebsocketTransportMethod.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withWebhookString(self):
        result = WebsocketTransportMethod.fromStr('webhook')
        assert result is WebsocketTransportMethod.WEBHOOK

    def test_fromStr_withWebsocketString(self):
        result = WebsocketTransportMethod.fromStr('websocket')
        assert result is WebsocketTransportMethod.WEBSOCKET

    def test_fromStr_withNone(self):
        result: Optional[WebsocketTransportMethod] = None
        exception: Optional[Exception] = None

        try:
            result = WebsocketTransportMethod.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withWhitespaceString(self):
        result: Optional[WebsocketTransportMethod] = None
        exception: Optional[Exception] = None

        try:
            result = WebsocketTransportMethod.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_toStr_withWebhook(self):
        string = WebsocketTransportMethod.WEBHOOK.toStr()
        assert string == 'webhook'

    def test_toStr_withWebsocket(self):
        string = WebsocketTransportMethod.WEBSOCKET.toStr()
        assert string == 'websocket'
