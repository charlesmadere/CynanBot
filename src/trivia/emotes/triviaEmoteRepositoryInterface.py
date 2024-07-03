from abc import ABC, abstractmethod


class TriviaEmoteRepositoryInterface(ABC):

    @abstractmethod
    async def getEmoteIndexFor(self, twitchChannelId: str) -> int | None:
        pass

    @abstractmethod
    async def setEmoteIndexFor(self, emoteIndex: int, twitchChannelId: str):
        pass
