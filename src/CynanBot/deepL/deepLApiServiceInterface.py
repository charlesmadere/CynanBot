from abc import ABC, abstractmethod

from CynanBot.deepL.deepLTranslationRequest import DeepLTranslationRequest
from CynanBot.deepL.deepLTranslationResponses import DeepLTranslationResponses


class DeepLApiServiceInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        request: DeepLTranslationRequest
    ) -> DeepLTranslationResponses:
        pass
