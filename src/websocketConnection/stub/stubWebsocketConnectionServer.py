from typing import Any

from ..websocketConnectionServerInterface import WebsocketConnectionServerInterface


class StubWebsocketConnectionServer(WebsocketConnectionServerInterface):

    async def clearCaches(self):
        # this method is intentionally empty
        pass

    async def sendEvent(
        self,
        twitchChannel: str,
        eventType: str,
        eventData: dict[Any, Any]
    ):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass
