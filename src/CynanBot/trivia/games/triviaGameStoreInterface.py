from abc import ABC, abstractmethod
from typing import List, Optional

from CynanBot.trivia.games.absTriviaGameState import AbsTriviaGameState
from CynanBot.trivia.games.superTriviaGameState import SuperTriviaGameState
from CynanBot.trivia.games.triviaGameState import TriviaGameState


class TriviaGameStoreInterface(ABC):

    @abstractmethod
    async def add(self, state: AbsTriviaGameState):
        pass

    @abstractmethod
    async def getAll(self) -> List[AbsTriviaGameState]:
        pass

    @abstractmethod
    async def getNormalGame(self, twitchChannel: str, userId: str) -> Optional[TriviaGameState]:
        pass

    @abstractmethod
    async def getNormalGames(self) -> List[TriviaGameState]:
        pass

    @abstractmethod
    async def getSuperGame(self, twitchChannel: str) -> Optional[SuperTriviaGameState]:
        pass

    @abstractmethod
    async def getSuperGames(self) -> List[SuperTriviaGameState]:
        pass

    @abstractmethod
    async def getTwitchChannelsWithActiveSuperGames(self) -> List[str]:
        pass

    @abstractmethod
    async def removeNormalGame(self, twitchChannel: str, userId: str) -> bool:
        pass

    @abstractmethod
    async def removeSuperGame(self, twitchChannel: str) -> bool:
        pass
