from abc import ABC, abstractmethod
from typing import Any

from ..models.absTtsProperties import AbsTtsProperties
from ...tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTtsProperties(
        self,
        configurationJson: dict[str, Any],
        provider: TtsProvider
    ) -> AbsTtsProperties:
        pass

    @abstractmethod
    async def serializeTtsProperties(
        self,
        ttsProperties: AbsTtsProperties
    ) -> dict[str, Any]:
        pass
