from abc import ABC, abstractmethod

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion


class TriviaQuestionPresenterInterface(ABC):

    @abstractmethod
    async def getCorrectAnswerBool(
        self,
        triviaQuestion: TrueFalseTriviaQuestion
    ) -> bool:
        pass

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
