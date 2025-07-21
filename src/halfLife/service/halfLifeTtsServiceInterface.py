from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozenlist import FrozenList

from ..models.halfLifeVoice import HalfLifeVoice
from ...misc.clearable import Clearable


class HalfLifeTtsServiceInterface(Clearable, ABC):

    @dataclass(frozen = True)
    class SoundFile:
        voice: HalfLifeVoice
        path: str

    @abstractmethod
    async def findSoundFiles(
        self,
        voice: HalfLifeVoice | None,
        message: str | None,
    ) -> FrozenList[SoundFile] | None:
        pass

    @abstractmethod
    async def getWavs(
        self,
        voice: HalfLifeVoice,
        message: str | None,
    ) -> FrozenList[str] | None:
        pass
