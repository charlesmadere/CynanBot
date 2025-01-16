from abc import ABC, abstractmethod

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion


class OpenTriviaDatabaseQuestionFetcherInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self, twitchChannelId: str) -> OpenTriviaDatabaseQuestion:
        pass
