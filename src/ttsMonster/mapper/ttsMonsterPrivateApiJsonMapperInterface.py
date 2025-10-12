from abc import ABC, abstractmethod
from typing import Any

from ..models.ttsMonsterDonationPrefixConfig import TtsMonsterDonationPrefixConfig
from ..models.ttsMonsterPrivateApiTtsData import TtsMonsterPrivateApiTtsData
from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from ..models.ttsMonsterVoice import TtsMonsterVoice


class TtsMonsterPrivateApiJsonMapperInterface(ABC):

    @abstractmethod
    async def parseDonationPrefixConfig(
        self,
        string: str | Any | None
    ) -> TtsMonsterDonationPrefixConfig | None:
        pass

    @abstractmethod
    async def parseTtsData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsData | None:
        pass

    @abstractmethod
    async def parseTtsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsResponse | None:
        pass

    @abstractmethod
    async def parseVoice(
        self,
        string: str | Any | None
    ) -> TtsMonsterVoice | None:
        pass

    @abstractmethod
    async def requireDonationPrefixConfig(
        self,
        string: str | Any | None
    ) -> TtsMonsterDonationPrefixConfig:
        pass

    @abstractmethod
    async def requireVoice(
        self,
        string: str | Any | None
    ) -> TtsMonsterVoice:
        pass

    @abstractmethod
    async def serializeDonationPrefixConfig(
        self,
        donationPrefixConfig: TtsMonsterDonationPrefixConfig
    ) -> str:
        pass

    @abstractmethod
    async def serializeGenerateTtsJsonBody(
        self,
        key: str,
        message: str,
        userId: str,
    ) -> dict[str, Any]:
        pass

    @abstractmethod
    async def serializeVoice(
        self,
        voice: TtsMonsterVoice
    ) -> str:
        pass
