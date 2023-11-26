from abc import abstractmethod
from typing import Any, Dict

from CynanBot.misc.clearable import Clearable


class WebsocketConnectionServerInterface(Clearable):

    @abstractmethod
    async def sendEvent(
        self,
        twitchChannel: str,
        eventType: str,
        eventData: Dict[Any, Any]
    ):
        pass

    @abstractmethod
    def start(self):
        pass
