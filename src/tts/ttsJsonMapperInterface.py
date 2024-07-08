from abc import ABC, abstractmethod
from typing import Any

from .ttsProvider import TtsProvider


class TtsJsonMapperInterface(ABC):

    @abstractmethod
    async def parseProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider | None:
        pass

    @abstractmethod
    async def requireProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider:
        pass

    @abstractmethod
    async def serializeProvider(
        self,
        ttsProvider: TtsProvider
    ) -> str:
        pass
