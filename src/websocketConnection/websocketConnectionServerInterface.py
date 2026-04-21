from abc import ABC, abstractmethod
from typing import Any

from .websocketEventType import WebsocketEventType
from ..misc.startable import Startable


class WebsocketConnectionServerInterface(Startable, ABC):

    @abstractmethod
    def submitEvent(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        eventType: WebsocketEventType,
        eventData: dict[str, Any],
    ):
        pass
