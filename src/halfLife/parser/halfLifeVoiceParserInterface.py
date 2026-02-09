from abc import ABC, abstractmethod
from typing import Any

from ..models.halfLifeVoice import HalfLifeVoice


class HalfLifeVoiceParserInterface(ABC):

    @abstractmethod
    def parseVoice(self, voiceString: str | Any | None) -> HalfLifeVoice | None:
        pass

    @abstractmethod
    def requireVoice(self, voiceString: str | Any | None) -> HalfLifeVoice:
        pass

    @abstractmethod
    def serializeVoice(self, voice: HalfLifeVoice) -> str:
        pass
