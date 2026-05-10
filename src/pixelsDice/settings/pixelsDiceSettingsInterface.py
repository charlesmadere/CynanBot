from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class PixelsDiceSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass

    @abstractmethod
    async def reportToChat(self) -> bool:
        pass

    @abstractmethod
    async def requireDiceName(self) -> str:
        pass
