from abc import ABC, abstractmethod
from typing import Any

from .deepLTranslationRequest import DeepLTranslationRequest
from .deepLTranslationResponse import DeepLTranslationResponse
from .deepLTranslationResponses import DeepLTranslationResponses


class DeepLJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTranslationResponse(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> DeepLTranslationResponse | None:
        pass

    @abstractmethod
    async def parseTranslationResponses(
        self,
        jsonContents: dict[str, Any] | Any | None,
    ) -> DeepLTranslationResponses | None:
        pass

    @abstractmethod
    async def serializeTranslationRequest(
        self,
        request: DeepLTranslationRequest,
    ) -> dict[str, Any]:
        pass
