from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class CrowdControlSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def areSoundsEnabled(self) -> bool:
        pass

    @abstractmethod
    async def getActionLoopCooldownSeconds(self) -> float:
        pass

    @abstractmethod
    async def getMaxGigaShuffleCount(self) -> int:
        pass

    @abstractmethod
    async def getMaxHandleAttempts(self) -> int:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int:
        pass

    @abstractmethod
    async def getMessageCooldownSeconds(self) -> float:
        pass

    @abstractmethod
    async def getMinGigaShuffleCount(self) -> int:
        pass

    @abstractmethod
    async def getSecondsToLive(self) -> int:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass

    @abstractmethod
    async def isGigaShuffleEnabled(self) -> bool:
        pass
