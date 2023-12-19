from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.trivia.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.startNewTriviaGameAction import StartNewTriviaGameAction


class TriviaGameBuilderInterface(ABC):

    @abstractmethod
    async def createNewTriviaGame(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> Optional[StartNewTriviaGameAction]:
        pass

    @abstractmethod
    async def createNewSuperTriviaGame(
        self,
        twitchChannel: str,
        numberOfGames: int = 1
    ) -> Optional[StartNewSuperTriviaGameAction]:
        pass
