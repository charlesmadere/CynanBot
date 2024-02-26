from abc import ABC, abstractmethod

from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslationRequest import GoogleTranslationRequest


class GoogleApiServiceInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        request: GoogleTranslationRequest
    ) -> GoogleTranslateTextResponse:
        pass
