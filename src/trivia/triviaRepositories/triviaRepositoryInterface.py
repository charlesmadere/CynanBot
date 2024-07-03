from abc import ABC, abstractmethod

from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..triviaFetchOptions import TriviaFetchOptions


class TriviaRepositoryInterface(ABC):

    @abstractmethod
    async def fetchTrivia(
        self,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions
    ) -> AbsTriviaQuestion | None:
        pass

    @abstractmethod
    def startSpooler(self):
        pass
