from abc import ABC, abstractmethod

from frozenlist import FrozenList


class TtsMonsterHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> FrozenList[str] | None:
        pass
