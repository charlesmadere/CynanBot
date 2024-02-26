from abc import ABC, abstractmethod

from CynanBot.google.googleTextSynthesisResponse import \
    GoogleTextSynthesisResponse
from CynanBot.google.googleTextSynthesizeRequest import \
    GoogleTextSynthesizeRequest
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslationRequest import GoogleTranslationRequest


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
