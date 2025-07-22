from abc import ABC, abstractmethod

from frozendict import frozendict

from ..models.halfLifeVoice import HalfLifeVoice
from ...misc.clearable import Clearable


class HalfLifeSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getDefaultVoice(self) -> HalfLifeVoice:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def getVoiceVolumes(self) -> frozendict[HalfLifeVoice, int | None]:
        pass

    @abstractmethod
    async def requireFileExtension(self) -> str:
        pass

    @abstractmethod
    async def requireSoundsDirectory(self) -> str:
        pass
