from abc import ABC, abstractmethod

from ..models.microsoftSamVoice import MicrosoftSamVoice


class MicrosoftSamApiServiceInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        voice: MicrosoftSamVoice,
        message: str
    ) -> bytes:
        pass
