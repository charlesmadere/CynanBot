from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class RedemptionCounterSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def automaticallyPrintInChatAfterRedemption(self) -> bool:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
