from abc import ABC, abstractmethod

from CynanBot.deepL.deepLTranslationResponses import DeepLTranslationResponses
from CynanBot.deepL.deepLTranslationRequest import DeepLTranslationRequest


class DeepLApiServiceInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        request: DeepLTranslationRequest
    ) -> DeepLTranslationResponses:
        pass
