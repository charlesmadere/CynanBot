from abc import ABC, abstractmethod

from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.actions.startNewTriviaGameAction import \
    StartNewTriviaGameAction
from CynanBot.trivia.questions.triviaSource import TriviaSource

class TriviaGameBuilderInterface(ABC):

    @abstractmethod
    async def createNewTriviaGame(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str
    ) -> StartNewTriviaGameAction | None:
        pass

    @abstractmethod
    async def createNewSuperTriviaGame(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        numberOfGames: int = 1,
        requiredTriviaSource: TriviaSource | None = None
    ) -> StartNewSuperTriviaGameAction | None:
        pass
