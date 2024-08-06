from abc import ABC, abstractmethod

from .absOpenTriviaDatabaseQuestion import AbsOpenTriviaDatabaseQuestion


class OpenTriviaDatabaseApiServiceInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(
        self,
        twitchChannelId: str | None
    ) -> AbsOpenTriviaDatabaseQuestion:
        pass
