from abc import ABC, abstractmethod
from typing import Any

from ..models.shotgun.shotgunProviderUseParameters import ShotgunProviderUseParameters
from ..models.ttsProvider import TtsProvider


class TtsJsonMapperInterface(ABC):

    @abstractmethod
    async def asyncParseProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider | None:
        pass

    @abstractmethod
    async def asyncRequireProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider:
        pass

    @abstractmethod
    async def asyncSerializeProvider(
        self,
        ttsProvider: TtsProvider
    ) -> str:
        pass

    @abstractmethod
    def parseProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider | None:
        pass

    @abstractmethod
    def parseShotgunProviderUseParameters(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> ShotgunProviderUseParameters | None:
        pass

    @abstractmethod
    def requireProvider(
        self,
        ttsProvider: str | Any | None
    ) -> TtsProvider:
        pass

    @abstractmethod
    def serializeProvider(
        self,
        ttsProvider: TtsProvider
    ) -> str:
        pass
