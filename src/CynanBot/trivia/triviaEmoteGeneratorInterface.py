from abc import ABC, abstractmethod
from typing import Optional


class TriviaEmoteGeneratorInterface(ABC):

    @abstractmethod
    async def getCurrentEmoteFor(self, twitchChannel: str) -> str:
        pass

    @abstractmethod
    async def getNextEmoteFor(self, twitchChannel: str) -> str:
        pass

    @abstractmethod
    def getRandomEmote(self) -> str:
        pass

    @abstractmethod
    async def getValidatedAndNormalizedEmote(self, emote: Optional[str]) -> Optional[str]:
        pass
