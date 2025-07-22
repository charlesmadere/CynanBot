from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.halfLifeSoundFile import HalfLifeSoundFile
from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeTtsHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        voice: HalfLifeVoice | None,
        message: str | None,
    ) -> FrozenList[HalfLifeSoundFile] | None:
        pass
