from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.halfLifeSoundFile import HalfLifeSoundFile
from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeTtsServiceInterface(ABC):

    @abstractmethod
    async def findSoundFiles(
        self,
        voice: HalfLifeVoice | None,
        message: str | None,
    ) -> FrozenList[HalfLifeSoundFile] | None:
        pass
