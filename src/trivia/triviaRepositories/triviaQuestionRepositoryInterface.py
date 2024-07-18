from abc import ABC, abstractmethod

from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..triviaFetchOptions import TriviaFetchOptions


class TriviaQuestionRepositoryInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        pass

    @abstractmethod
    async def hasQuestionSetAvailable(self) -> bool:
        pass

    @property
    @abstractmethod
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        pass

    @property
    @abstractmethod
    def triviaSource(self) -> TriviaSource:
        pass
