from abc import ABC, abstractmethod


class TriviaEmoteGeneratorInterface(ABC):

    @abstractmethod
    async def getCurrentEmoteFor(self, twitchChannelId: str) -> str:
        pass

    @abstractmethod
    async def getNextEmoteFor(self, twitchChannelId: str) -> str:
        pass

    @abstractmethod
    def getRandomEmote(self) -> str:
        pass

    @abstractmethod
    async def getValidatedAndNormalizedEmote(self, emote: str | None) -> str | None:
        pass
