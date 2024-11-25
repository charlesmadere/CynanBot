from abc import ABC, abstractmethod
from typing import Any


class WebsocketConnectionServerInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitEvent(
        self,
        twitchChannel: str,
        eventType: str,
        eventData: dict[str, Any]
    ):
        pass
