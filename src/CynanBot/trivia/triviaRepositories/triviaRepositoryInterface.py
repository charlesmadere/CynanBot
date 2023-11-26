from abc import ABC, abstractmethod
from typing import Optional

from trivia.absTriviaQuestion import AbsTriviaQuestion
from trivia.triviaFetchOptions import TriviaFetchOptions


class TriviaRepositoryInterface(ABC):

    @abstractmethod
    async def fetchTrivia(
        self,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions
    ) -> Optional[AbsTriviaQuestion]:
        pass

    @abstractmethod
    def startSpooler(self):
        pass
