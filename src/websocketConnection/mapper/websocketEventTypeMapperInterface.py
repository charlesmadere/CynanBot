from abc import ABC, abstractmethod

from ..websocketEventType import WebsocketEventType


class WebsocketEventTypeMapperInterface(ABC):

    @abstractmethod
    def serializeEventType(self, eventType: WebsocketEventType) -> str:
        pass
