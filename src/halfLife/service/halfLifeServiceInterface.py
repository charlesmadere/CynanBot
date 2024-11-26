from abc import ABC, abstractmethod

from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeServiceInterface(ABC):

    @abstractmethod
    def getWavs(
        self,
        directory: str,
        text: str,
        voice: HalfLifeVoice
    ) -> list[str] | None:
        pass
