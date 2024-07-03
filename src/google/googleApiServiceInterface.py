from abc import ABC, abstractmethod

from .googleTextSynthesisResponse import GoogleTextSynthesisResponse
from .googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from .googleTranslateTextResponse import GoogleTranslateTextResponse
from .googleTranslationRequest import GoogleTranslationRequest


class GoogleApiServiceInterface(ABC):

    @abstractmethod
    async def textToSpeech(
        self,
        request: GoogleTextSynthesizeRequest
    ) -> GoogleTextSynthesisResponse:
        pass

    @abstractmethod
    async def translate(
        self,
        request: GoogleTranslationRequest
    ) -> GoogleTranslateTextResponse:
        pass
