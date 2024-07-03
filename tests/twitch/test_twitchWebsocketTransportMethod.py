from typing import Optional

from src.twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod


class TestTwitchWebsocketTransportMethod():

    def test_fromStr_withEmptyString(self):
        result: Optional[TwitchWebsocketTransportMethod] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchWebsocketTransportMethod.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withWebhookString(self):
        result = TwitchWebsocketTransportMethod.fromStr('webhook')
        assert result is TwitchWebsocketTransportMethod.WEBHOOK

    def test_fromStr_withWebsocketString(self):
        result = TwitchWebsocketTransportMethod.fromStr('websocket')
        assert result is TwitchWebsocketTransportMethod.WEBSOCKET

    def test_fromStr_withNone(self):
        result: Optional[TwitchWebsocketTransportMethod] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchWebsocketTransportMethod.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withWhitespaceString(self):
        result: Optional[TwitchWebsocketTransportMethod] = None
        exception: Optional[Exception] = None

        try:
            result = TwitchWebsocketTransportMethod.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_toStr_withWebhook(self):
        string = TwitchWebsocketTransportMethod.WEBHOOK.toStr()
        assert string == 'webhook'

    def test_toStr_withWebsocket(self):
        string = TwitchWebsocketTransportMethod.WEBSOCKET.toStr()
        assert string == 'websocket'
