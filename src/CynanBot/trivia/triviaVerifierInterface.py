from abc import ABC, abstractmethod
from typing import Optional

from trivia.absTriviaQuestion import AbsTriviaQuestion
from trivia.triviaContentCode import TriviaContentCode
from trivia.triviaFetchOptions import TriviaFetchOptions


class TriviaVerifierInterface(ABC):

    @abstractmethod
    async def checkContent(
        self,
        question: Optional[AbsTriviaQuestion],
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
