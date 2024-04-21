from abc import ABC, abstractmethod
from typing import Any

from CynanBot.deepL.deepLTranslationRequest import DeepLTranslationRequest
from CynanBot.deepL.deepLTranslationResponse import DeepLTranslationResponse
from CynanBot.deepL.deepLTranslationResponses import DeepLTranslationResponses


class DeepLJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTranslationResponse(
        self,
        jsonContents: dict[str, Any] | None | Any
    ) -> DeepLTranslationResponse | None:
        pass

    @abstractmethod
    async def parseTranslationResponses(
        self,
        jsonContents: dict[str, Any] | None | Any
    ) -> DeepLTranslationResponses | None:
        pass

    @abstractmethod
    async def serializeTranslationRequest(
        self,
        request: DeepLTranslationRequest
    ) -> dict[str, Any]:
        pass
