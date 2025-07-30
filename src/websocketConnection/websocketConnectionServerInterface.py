from abc import ABC, abstractmethod
from typing import Any

from .websocketEventType import WebsocketEventType


class WebsocketConnectionServerInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitEvent(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        eventType: WebsocketEventType,
        eventData: dict[str, Any],
    ):
        pass
