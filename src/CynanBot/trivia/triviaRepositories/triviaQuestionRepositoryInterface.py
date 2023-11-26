from abc import ABC, abstractmethod
from typing import Set

from CynanBot.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaSource import TriviaSource
from CynanBot.trivia.triviaType import TriviaType


class TriviaQuestionRepositoryInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        pass

    @abstractmethod
    def getSupportedTriviaTypes(self) -> Set[TriviaType]:
        pass

    @abstractmethod
    def getTriviaSource(self) -> TriviaSource:
        pass

    @abstractmethod
    async def hasQuestionSetAvailable(self) -> bool:
        pass
