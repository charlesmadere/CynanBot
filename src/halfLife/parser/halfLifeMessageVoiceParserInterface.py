from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeMessageVoiceParserInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class Result:
        message: str
        voice: HalfLifeVoice

    @abstractmethod
    async def determineVoiceFromMessage(
        self,
        message: str | None,
    ) -> Result | None:
        pass
