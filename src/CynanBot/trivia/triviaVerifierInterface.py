from abc import ABC, abstractmethod

from CynanBot.trivia.content.triviaContentCode import TriviaContentCode
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions


class TriviaVerifierInterface(ABC):

    @abstractmethod
    async def checkContent(
        self,
        question: AbsTriviaQuestion | None,
        triviaFetchOptions: TriviaFetchOptions
    ) -> TriviaContentCode:
        pass

    @abstractmethod
    async def checkHistory(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions
    ) -> TriviaContentCode:
        pass
