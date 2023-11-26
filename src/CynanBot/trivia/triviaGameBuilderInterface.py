from abc import ABC, abstractmethod
from typing import Optional

from trivia.startNewSuperTriviaGameAction import StartNewSuperTriviaGameAction
from trivia.startNewTriviaGameAction import StartNewTriviaGameAction


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
