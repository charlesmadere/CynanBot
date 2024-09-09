from abc import ABC, abstractmethod

from ..models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice


class TtsMonsterWebsiteVoiceMapperInterface(ABC):

    @abstractmethod
    async def map(self, apiVoiceId: str) -> TtsMonsterWebsiteVoice | None:
        pass
