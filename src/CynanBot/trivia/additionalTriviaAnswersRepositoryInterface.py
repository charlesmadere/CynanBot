from abc import ABC, abstractmethod
from typing import List, Optional

from trivia.additionalTriviaAnswers import AdditionalTriviaAnswers
from trivia.triviaSource import TriviaSource
from trivia.triviaType import TriviaType


class AdditionalTriviaAnswersRepositoryInterface(ABC):

    @abstractmethod
    async def addAdditionalTriviaAnswer(
        self,
        additionalAnswer: str,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaType
    ) -> AdditionalTriviaAnswers:
        pass

    @abstractmethod
    async def addAdditionalTriviaAnswers(
        self,
        currentAnswers: List[str],
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaType
    ) -> bool:
        pass

    @abstractmethod
    async def deleteAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaType
    ) -> Optional[AdditionalTriviaAnswers]:
        pass

    @abstractmethod
    async def getAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaType
    ) -> Optional[AdditionalTriviaAnswers]:
        pass
