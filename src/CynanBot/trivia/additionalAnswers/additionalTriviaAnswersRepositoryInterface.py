from abc import ABC, abstractmethod

from CynanBot.trivia.additionalAnswers.additionalTriviaAnswers import \
    AdditionalTriviaAnswers
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource


class AdditionalTriviaAnswersRepositoryInterface(ABC):

    @abstractmethod
    async def addAdditionalTriviaAnswer(
        self,
        additionalAnswer: str,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ) -> AdditionalTriviaAnswers:
        pass

    @abstractmethod
    async def addAdditionalTriviaAnswers(
        self,
        currentAnswers: list[str],
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ) -> bool:
        pass

    @abstractmethod
    async def deleteAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ) -> AdditionalTriviaAnswers | None:
        pass

    @abstractmethod
    async def getAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ) -> AdditionalTriviaAnswers | None:
        pass
