from abc import ABC, abstractmethod

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion


class OpenTriviaDatabaseApiServiceInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(
        self,
        twitchChannelId: str | None
    ) -> OpenTriviaDatabaseQuestion:
        pass
