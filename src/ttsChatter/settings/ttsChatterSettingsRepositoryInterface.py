from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TtsChatterSettingsRepositoryInterface(Clearable, ABC):
    @abstractmethod
    async def useThreshold(self) -> int:
        pass

    @abstractmethod
    async def ttsOffThreshold(self) -> int:
        pass

    @abstractmethod
    async def ttsOnThreshold(self) -> int:
        pass

    @abstractmethod
    async def useMessageQueueing(self) -> bool:
        pass

    @abstractmethod
    async def subscriberOnly(self) -> bool:
        pass
