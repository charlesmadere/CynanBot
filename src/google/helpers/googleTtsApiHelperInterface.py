from abc import ABC, abstractmethod

from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest


class GoogleTtsApiHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        request: GoogleTextSynthesizeRequest,
    ) -> bytes | None:
        pass
