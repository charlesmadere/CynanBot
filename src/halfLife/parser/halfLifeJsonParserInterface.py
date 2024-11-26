from abc import ABC, abstractmethod
from typing import Any

from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeJsonParserInterface(ABC):

    @abstractmethod
    def parseVoice(self, jsonString: str | Any | None) -> HalfLifeVoice | None:
        pass

    @abstractmethod
    def requireVoice(self, jsonString: str | Any | None) -> HalfLifeVoice:
        pass

    @abstractmethod
    def serializeVoice(self, voice: HalfLifeVoice) -> str:
        pass
