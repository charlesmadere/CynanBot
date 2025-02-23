from abc import ABC, abstractmethod
from typing import Any

from ..models.ttsMonsterVoice import TtsMonsterVoice


class TtsMonsterVoiceParserInterface(ABC):

    @abstractmethod
    def parseVoice(self, jsonString: str | Any | None) -> TtsMonsterVoice | None:
        pass

    @abstractmethod
    def requireVoice(self, jsonString: str | Any | None) -> TtsMonsterVoice:
        pass

    @abstractmethod
    def serializeVoice(self, voice: TtsMonsterVoice):
        pass
