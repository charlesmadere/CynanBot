from abc import ABC, abstractmethod

from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse


class TtsMonsterPrivateApiServiceInterface(ABC):

    @abstractmethod
    async def fetchGeneratedTts(
        self,
        ttsUrl: str,
    ) -> bytes:
        pass

    @abstractmethod
    async def generateTts(
        self,
        key: str,
        message: str,
        userId: str,
    ) -> TtsMonsterPrivateApiTtsResponse:
        pass
