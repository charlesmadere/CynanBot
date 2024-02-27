from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.actions.startNewTriviaGameAction import \
    StartNewTriviaGameAction


class TriviaGameBuilderInterface(ABC):

    @abstractmethod
    async def createNewTriviaGame(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str
    ) -> Optional[StartNewTriviaGameAction]:
        pass

    @abstractmethod
    async def createNewSuperTriviaGame(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        numberOfGames: int = 1
    ) -> Optional[StartNewSuperTriviaGameAction]:
        pass
