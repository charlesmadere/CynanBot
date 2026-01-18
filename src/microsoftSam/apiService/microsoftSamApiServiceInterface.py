from abc import ABC, abstractmethod

from ..models.microsoftSamVoice import MicrosoftSamVoice


class MicrosoftSamApiServiceInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        voice: MicrosoftSamVoice,
        text: str,
    ) -> bytes:
        pass
