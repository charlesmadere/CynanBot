from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class TtsSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getGoogleVolumeGainDb(self) -> float | None:
        pass

    @abstractmethod
    async def getMaximumMessageSize(self) -> int:
        pass

    @abstractmethod
    async def getTtsDelayBetweenSeconds(self) -> float:
        pass

    @abstractmethod
    async def getTtsTimeoutSeconds(self) -> float:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass

    @abstractmethod
    async def requireDecTalkPath(self) -> str:
        pass
