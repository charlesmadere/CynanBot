from src.twitch.api.websocket.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


class TestTwitchWebsocketTransportMethod:

    def test_toStr_withWebhook(self):
        string = TwitchWebsocketTransportMethod.WEBHOOK.toStr()
        assert string == 'webhook'

    def test_toStr_withWebsocket(self):
        string = TwitchWebsocketTransportMethod.WEBSOCKET.toStr()
        assert string == 'websocket'
