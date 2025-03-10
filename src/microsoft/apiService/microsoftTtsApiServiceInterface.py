from abc import ABC, abstractmethod

from ..models.microsoftTtsVoice import MicrosoftTtsVoice


class MicrosoftTtsApiServiceInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        voice: MicrosoftTtsVoice,
        message: str
    ) -> bytes:
        pass
