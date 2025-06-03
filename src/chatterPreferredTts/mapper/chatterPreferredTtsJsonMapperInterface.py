from abc import ABC, abstractmethod
from typing import Any

from ..models.absTtsProperties import AbsTtsProperties
from ...tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsJsonMapperInterface(ABC):

    @abstractmethod
    async def parsePreferredTts(
        self,
        configurationJson: dict[str, Any],
        provider: TtsProvider
    ) -> AbsTtsProperties:
        pass

    @abstractmethod
    async def serializePreferredTts(
        self,
        preferredTts: AbsTtsProperties
    ) -> dict[str, Any]:
        pass
