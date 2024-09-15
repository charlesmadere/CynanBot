from abc import ABC, abstractmethod
from typing import Any

from ..models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from ..models.ttsMonsterTtsResponse import TtsMonsterTtsResponse
from ..models.ttsMonsterUser import TtsMonsterUser
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ..models.ttsMonsterVoicesResponse import TtsMonsterVoicesResponse


class TtsMonsterJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTtsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterTtsResponse | None:
        pass

    @abstractmethod
    async def parseUser(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterUser | None:
        pass

    @abstractmethod
    async def parseVoice(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterVoice | None:
        pass

    @abstractmethod
    async def parseVoicesResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterVoicesResponse | None:
        pass

    @abstractmethod
    async def serializeTtsRequest(
        self,
        request: TtsMonsterTtsRequest
    ) -> dict[str, Any]:
        pass
