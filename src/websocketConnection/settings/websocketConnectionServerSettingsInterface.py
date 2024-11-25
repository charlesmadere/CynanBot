from abc import abstractmethod

from ...misc.clearable import Clearable


class WebsocketConnectionServerSettingsInterface(Clearable):

    @abstractmethod
    async def getEventTimeToLiveSeconds(self) -> int:
        pass

    @abstractmethod
    async def getHost(self) -> str:
        pass

    @abstractmethod
    async def getPort(self) -> int:
        pass
