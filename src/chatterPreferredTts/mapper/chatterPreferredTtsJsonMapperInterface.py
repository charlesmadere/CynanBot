from abc import ABC, abstractmethod
from typing import Any

from ..models.absPreferredTts import AbsPreferredTts
from ..models.preferredTtsProvider import PreferredTtsProvider


class ChatterPreferredTtsJsonMapperInterface(ABC):

    @abstractmethod
    async def parsePreferredTts(
        self,
        jsonData: dict[str, Any] | Any | None
    ) -> AbsPreferredTts:
        pass

    @abstractmethod
    async def parsePreferredTtsProvider(
        self,
        string: str | Any | None
    ) -> PreferredTtsProvider:
        pass

    @abstractmethod
    async def serializePreferredTts(
        self,
        preferredTts: AbsPreferredTts
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializePreferredTtsProvider(
        self,
        provider: PreferredTtsProvider
    ) -> str:
        pass
