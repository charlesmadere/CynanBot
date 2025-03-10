from abc import ABC, abstractmethod

from ..models.microsoftTtsVoice import MicrosoftTtsVoice


class MicrosoftTtsApiHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        voice: MicrosoftTtsVoice,
        message: str | None
    ) -> bytes | None:
        pass
