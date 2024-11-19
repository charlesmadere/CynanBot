from abc import ABC, abstractmethod
from typing import Any

from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsJsonParserInterface(ABC):

    @abstractmethod
    def parseVoice(self, jsonString: str | Any | None) -> StreamElementsVoice | None:
        pass

    @abstractmethod
    def requireVoice(self, jsonString: str | Any | None) -> StreamElementsVoice:
        pass

    @abstractmethod
    def serializeVoice(self, voice: StreamElementsVoice) -> str:
        pass
