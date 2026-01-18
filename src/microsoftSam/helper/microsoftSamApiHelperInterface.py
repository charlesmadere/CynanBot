from abc import ABC, abstractmethod

from ..models.microsoftSamVoice import MicrosoftSamVoice


class MicrosoftSamApiHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        voice: MicrosoftSamVoice,
        message: str | None,
    ) -> bytes | None:
        pass
