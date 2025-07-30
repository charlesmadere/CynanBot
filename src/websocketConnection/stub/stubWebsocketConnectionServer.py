from typing import Any

from ..websocketConnectionServerInterface import WebsocketConnectionServerInterface
from ..websocketEventType import WebsocketEventType


class StubWebsocketConnectionServer(WebsocketConnectionServerInterface):

    def start(self):
        # this method is intentionally empty
        pass

    def submitEvent(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        eventType: WebsocketEventType,
        eventData: dict[str, Any],
    ):
        # this method is intentionally empty
        pass
