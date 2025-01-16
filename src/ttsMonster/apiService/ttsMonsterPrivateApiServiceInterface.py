from abc import ABC, abstractmethod

from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse


class TtsMonsterPrivateApiServiceInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        key: str,
        message: str,
        userId: str
    ) -> TtsMonsterPrivateApiTtsResponse:
        pass
