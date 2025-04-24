from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeTtsHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        voice: HalfLifeVoice | None,
        message: str | None
    ) -> FrozenList[str] | None:
        pass
