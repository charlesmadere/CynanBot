from abc import ABC, abstractmethod
from typing import Any

from ..models.absPreferredTts import AbsPreferredTts
from ...tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsJsonMapperInterface(ABC):

    @abstractmethod
    async def parsePreferredTts(
        self,
        configurationJson: dict[str, Any],
        provider: TtsProvider
    ) -> AbsPreferredTts:
        pass

    @abstractmethod
    async def serializePreferredTts(
        self,
        preferredTts: AbsPreferredTts
    ) -> dict[str, Any]:
        pass