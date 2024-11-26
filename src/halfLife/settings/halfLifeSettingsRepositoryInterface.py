from abc import abstractmethod

from ..models.halfLifeVoice import HalfLifeVoice
from ...misc.clearable import Clearable


class HalfLifeSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getDefaultVoice(self) -> HalfLifeVoice:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def getSoundsDirectory(self) -> str:
        pass