from abc import ABC, abstractmethod

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseSessionToken import OpenTriviaDatabaseSessionToken


class OpenTriviaDatabaseApiServiceInterface(ABC):

    @abstractmethod
    async def fetchSessionToken(self) -> OpenTriviaDatabaseSessionToken:
        pass

    @abstractmethod
    async def fetchTriviaQuestion(
        self,
        sessionToken: str | None,
        twitchChannelId: str
    ) -> OpenTriviaDatabaseQuestion:
        pass
