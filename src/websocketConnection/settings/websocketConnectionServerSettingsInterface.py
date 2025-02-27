from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class WebsocketConnectionServerSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getEventTimeToLiveSeconds(self) -> int:
        pass

    @abstractmethod
    async def getHost(self) -> str:
        pass

    @abstractmethod
    async def getPort(self) -> int:
        pass
