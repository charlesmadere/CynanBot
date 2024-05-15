from abc import ABC, abstractmethod

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion


class TriviaQuestionPresenterInterface(ABC):

    @abstractmethod
    async def toString(self, triviaQuestion: AbsTriviaQuestion) -> str:
        pass
