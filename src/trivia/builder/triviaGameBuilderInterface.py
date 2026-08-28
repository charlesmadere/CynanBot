from abc import ABC, abstractmethod

from ..actions.startNewSuperTriviaGameAction import StartNewSuperTriviaGameAction
from ..actions.startNewTriviaGameAction import StartNewTriviaGameAction
from ..questions.triviaSource import TriviaSource
from ...users.userInterface import UserInterface


class TriviaGameBuilderInterface(ABC):

    @abstractmethod
    async def createNewTriviaGame(
        self,
        chatterUserId: str,
        chatterUserLogin: str,
        chatterUserName: str,
        twitchChannelId: str,
        twitchUser: UserInterface,
    ) -> StartNewTriviaGameAction | None:
        pass

    @abstractmethod
    async def createNewSuperTriviaGame(
        self,
        twitchChannelId: str,
        twitchUser: UserInterface,
        numberOfGames: int = 1,
        requiredTriviaSource: TriviaSource | None = None,
    ) -> StartNewSuperTriviaGameAction | None:
        pass
