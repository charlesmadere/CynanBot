from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeServiceInterface(ABC):

    @abstractmethod
    async def getWavs(
        self,
        directory: str,
        text: str,
        voice: HalfLifeVoice
    ) -> FrozenList[str]:
        pass
