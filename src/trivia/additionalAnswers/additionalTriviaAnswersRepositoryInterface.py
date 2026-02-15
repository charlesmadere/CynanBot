from abc import ABC, abstractmethod

from .additionalTriviaAnswers import AdditionalTriviaAnswers
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource


class AdditionalTriviaAnswersRepositoryInterface(ABC):

    @abstractmethod
    async def addAdditionalTriviaAnswer(
        self,
        additionalAnswer: str,
        triviaId: str,
        userId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource,
    ) -> AdditionalTriviaAnswers:
        pass

    @abstractmethod
    async def addAdditionalTriviaAnswers(
        self,
        currentAnswers: list[str],
        triviaId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource,
    ) -> bool:
        pass

    @abstractmethod
    async def deleteAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource,
    ) -> AdditionalTriviaAnswers | None:
        pass

    @abstractmethod
    async def getAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource,
    ) -> AdditionalTriviaAnswers | None:
        pass
