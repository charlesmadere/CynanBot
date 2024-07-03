from abc import ABC, abstractmethod

from .questions.absTriviaQuestion import AbsTriviaQuestion


class TriviaQuestionPresenterInterface(ABC):

    @abstractmethod
    async def getCorrectAnswers(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delimiter: str = '; '
    ) -> str:
        pass

    @abstractmethod
    async def getPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delimiter: str = ' '
    ) -> str:
        pass

    @abstractmethod
    async def getResponses(
        self,
        triviaQuestion: AbsTriviaQuestion
    ) -> list[str]:
        pass
