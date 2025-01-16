from src.twitch.api.models.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


class TestTwitchWebsocketTransportMethod:

    def test_toStr_withConduit(self):
        string = TwitchWebsocketTransportMethod.CONDUIT.toStr()
        assert string == 'conduit'

    def test_toStr_withWebhook(self):
        string = TwitchWebsocketTransportMethod.WEBHOOK.toStr()
        assert string == 'webhook'

    def test_toStr_withWebsocket(self):
        string = TwitchWebsocketTransportMethod.WEBSOCKET.toStr()
        assert string == 'websocket'
