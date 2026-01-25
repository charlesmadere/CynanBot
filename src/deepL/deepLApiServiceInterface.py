from abc import ABC, abstractmethod

from .deepLTranslationRequest import DeepLTranslationRequest
from .deepLTranslationResponses import DeepLTranslationResponses


class DeepLApiServiceInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        request: DeepLTranslationRequest,
    ) -> DeepLTranslationResponses:
        pass
