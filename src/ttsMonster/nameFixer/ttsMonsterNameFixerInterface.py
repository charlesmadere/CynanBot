from abc import ABC, abstractmethod


class TtsMonsterNameFixerInterface(ABC):

    @abstractmethod
    async def getWebsiteName(self, apiVoiceId: str) -> str | None:
        pass
