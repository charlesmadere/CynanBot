from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaContentCode import TriviaContentCode
from CynanBot.trivia.triviaQuestionReference import TriviaQuestionReference


class TriviaHistoryRepositoryInterface(ABC):

    @abstractmethod
    async def getMostRecentTriviaQuestionDetails(
        self,
        emote: str,
        twitchChannel: str
    ) -> Optional[TriviaQuestionReference]:
        pass

    @abstractmethod
    async def verify(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        twitchChannel: str
    ) -> TriviaContentCode:
        pass
