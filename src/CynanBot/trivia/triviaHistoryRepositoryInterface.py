from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionReference import \
    TriviaQuestionReference
from CynanBot.trivia.content.triviaContentCode import TriviaContentCode


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
