from abc import ABC, abstractmethod
from typing import Any

from .models.microsoftSamVoice import MicrosoftSamVoice


class MicrosoftSamJsonParserInterface(ABC):

    @abstractmethod
    def parseVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice | None:
        pass

    @abstractmethod
    def requireVoice(self, jsonString: str | Any | None) -> MicrosoftSamVoice:
        pass

    @abstractmethod
    def serializeVoice(self, voice: MicrosoftSamVoice):
        pass