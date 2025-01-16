from abc import ABC, abstractmethod

from ..websocketEventType import WebsocketEventType


class WebsocketEventTypeMapperInterface(ABC):

    @abstractmethod
    def toString(self, eventType: WebsocketEventType) -> str:
        pass
