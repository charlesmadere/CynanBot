from abc import ABC, abstractmethod

from .content.triviaContentCode import TriviaContentCode
from .questions.absTriviaQuestion import AbsTriviaQuestion
from .triviaFetchOptions import TriviaFetchOptions


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
