from abc import ABC, abstractmethod

from ..models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from ..models.ttsMonsterTtsResponse import TtsMonsterTtsResponse
from ..models.ttsMonsterVoicesResponse import TtsMonsterVoicesResponse


class TtsMonsterApiServiceInterface(ABC):

    @abstractmethod
    async def fetchGeneratedTts(self, ttsUrl: str) -> bytes:
        pass

    @abstractmethod
    async def generateTts(
        self,
        apiToken: str,
        request: TtsMonsterTtsRequest
    ) -> TtsMonsterTtsResponse:
        pass

    @abstractmethod
    async def getVoices(self, apiToken: str) -> TtsMonsterVoicesResponse:
        pass
