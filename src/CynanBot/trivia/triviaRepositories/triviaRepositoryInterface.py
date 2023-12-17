from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions


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
