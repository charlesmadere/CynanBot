from abc import ABC, abstractmethod

from ..misc.clearable import Clearable


class PixelsDiceSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getDiceName(self) -> str | None:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
