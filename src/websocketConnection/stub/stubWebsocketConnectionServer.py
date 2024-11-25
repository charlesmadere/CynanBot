from typing import Any

from ..websocketConnectionServerInterface import WebsocketConnectionServerInterface


class StubWebsocketConnectionServer(WebsocketConnectionServerInterface):

    def start(self):
        # this method is intentionally empty
        pass

    def submitEvent(
        self,
        twitchChannel: str,
        eventType: str,
        eventData: dict[str, Any]
    ):
        # this method is intentionally empty
        pass
