from abc import ABC, abstractmethod

from ..models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice


class TtsMonsterWebsiteVoiceMapperInterface(ABC):

    @abstractmethod
    async def fromApiVoiceId(self, apiVoiceId: str) -> TtsMonsterWebsiteVoice | None:
        pass

    @abstractmethod
    async def fromWebsiteName(self, websiteName: str) -> TtsMonsterWebsiteVoice:
        pass
