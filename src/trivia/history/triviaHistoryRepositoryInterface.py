from abc import ABC, abstractmethod

from ..content.triviaContentCode import TriviaContentCode
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaQuestionReference import TriviaQuestionReference


class TriviaHistoryRepositoryInterface(ABC):

    @abstractmethod
    async def getMostRecentTriviaQuestionDetails(
        self,
        emote: str,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> TriviaQuestionReference | None:
        pass

    @abstractmethod
    async def verify(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> TriviaContentCode:
        pass
