from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.websocket.websocketCondition import WebsocketCondition
from CynanBot.twitch.websocket.websocketConnectionStatus import \
    WebsocketConnectionStatus
from CynanBot.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBot.twitch.websocket.websocketPayload import WebsocketPayload
from CynanBot.twitch.websocket.websocketSession import WebsocketSession
from CynanBot.twitch.websocket.websocketSubscription import \
    WebsocketSubscription
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.twitch.websocket.websocketTransport import WebsocketTransport


class TestTwitchWebsocketPayload():

    def __createEvent(self) -> WebsocketEvent:
        return WebsocketEvent()

    def __createSession(self) -> WebsocketSession:
        return WebsocketSession(
            keepAliveTimeoutSeconds = 100,
            connectedAt = SimpleDateTime(),
            reconnectUrl = None,
            sessionId = 'abc123',
            status = WebsocketConnectionStatus.CONNECTED
        )

    def __createSubscription(self) -> WebsocketSubscription:
        return WebsocketSubscription(
            cost = 100,
            createdAt = SimpleDateTime(),
            subscriptionId = 'qwerty',
            version = '1',
            condition = WebsocketCondition(),
            status = WebsocketConnectionStatus.CONNECTED,
            subscriptionType = WebsocketSubscriptionType.CHEER,
            transport = WebsocketTransport()
        )

    def test_isEmpty_withDefaultConstructor(self):
        payload = WebsocketPayload()
        assert payload.isEmpty() is True

    def test_isEmpty_withEvent(self):
        payload = WebsocketPayload(event = self.__createEvent())
        assert payload.isEmpty() is False

    def test_isEmpty_withSession(self):
        payload = WebsocketPayload(session = self.__createSession())
        assert payload.isEmpty() is False

    def test_isEmpty_withSubscription(self):
        payload = WebsocketPayload(subscription = self.__createSubscription())
        assert payload.isEmpty() is False
