from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.halfLifeVoice import HalfLifeVoice
from ...misc.clearable import Clearable


class HalfLifeTtsServiceInterface(Clearable, ABC):

    @abstractmethod
    async def getWavs(
        self,
        voice: HalfLifeVoice,
        directory: str,
        text: str
    ) -> FrozenList[str]:
        pass
