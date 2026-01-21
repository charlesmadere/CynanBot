from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.microsoftTtsVoice import MicrosoftTtsVoice


class MicrosoftTtsMessageVoiceParserInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class Result:
        voice: MicrosoftTtsVoice
        message: str

    @abstractmethod
    async def determineVoiceFromMessage(
        self,
        message: str | None,
    ) -> Result | None:
        pass
