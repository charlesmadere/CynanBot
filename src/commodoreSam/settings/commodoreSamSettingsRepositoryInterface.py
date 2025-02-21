from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class CommodoreSamSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getCommodoreSamExecutablePath(self) -> str | None:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def requireCommodoreSamExecutablePath(self) -> str:
        pass
