from abc import ABC, abstractmethod


class TtsMonsterHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> str | None:
        pass
