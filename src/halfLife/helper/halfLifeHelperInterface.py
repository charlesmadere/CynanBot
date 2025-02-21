from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        voice: HalfLifeVoice,
        message: str | None
    ) -> FrozenList[str] | None:
        pass
