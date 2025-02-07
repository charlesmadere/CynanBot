from abc import ABC, abstractmethod


class TtsMonsterPrivateApiHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> bytes | None:
        pass
