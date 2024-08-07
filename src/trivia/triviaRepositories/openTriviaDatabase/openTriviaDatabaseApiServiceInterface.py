from abc import ABC, abstractmethod

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseSessionToken import OpenTriviaDatabaseSessionToken


class OpenTriviaDatabaseApiServiceInterface(ABC):

    @abstractmethod
    async def fetchSessionToken(self) -> OpenTriviaDatabaseSessionToken:
        pass

    @abstractmethod
    async def fetchTriviaQuestion(self, twitchChannelId: str) -> OpenTriviaDatabaseQuestion:
        pass
