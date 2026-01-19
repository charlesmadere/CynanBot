from abc import ABC, abstractmethod

from ..models.googleTextSynthesisResponse import GoogleTextSynthesisResponse
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ..models.googleTranslateTextResponse import GoogleTranslateTextResponse
from ..models.googleTranslationRequest import GoogleTranslationRequest


class GoogleApiServiceInterface(ABC):

    @abstractmethod
    async def textToSpeech(
        self,
        request: GoogleTextSynthesizeRequest,
    ) -> GoogleTextSynthesisResponse:
        pass

    @abstractmethod
    async def translate(
        self,
        request: GoogleTranslationRequest,
    ) -> GoogleTranslateTextResponse:
        pass
