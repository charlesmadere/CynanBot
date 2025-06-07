from typing import Final

from frozenlist import FrozenList

from .absTriviaGameState import AbsTriviaGameState
from .superTriviaGameState import SuperTriviaGameState
from .triviaGameState import TriviaGameState
from .triviaGameStoreInterface import TriviaGameStoreInterface
from ..triviaExceptions import UnknownTriviaGameTypeException
from ...misc import utils as utils


class TriviaGameStore(TriviaGameStoreInterface):

    def __init__(self):
        self.__normalGameStates: Final[list[TriviaGameState]] = list()
        self.__superGameStates: Final[list[SuperTriviaGameState]] = list()

    async def add(
        self,
        state: AbsTriviaGameState
    ):
        if not isinstance(state, AbsTriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        if isinstance(state, TriviaGameState):
            await self.__addNormalGame(state)
        elif isinstance(state, SuperTriviaGameState):
            await self.__addSuperGame(state)
        else:
            raise UnknownTriviaGameTypeException(f'Unknown TriviaGameType ({state=}): \"{state.triviaGameType}\"')

    async def __addNormalGame(self, state: TriviaGameState):
        if not isinstance(state, TriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        self.__normalGameStates.append(state)

    async def __addSuperGame(self, state: SuperTriviaGameState):
        if not isinstance(state, SuperTriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        self.__superGameStates.append(state)

    async def getAll(self) -> FrozenList[AbsTriviaGameState]:
        normalGames = await self.getNormalGames()
        superGames = await self.getSuperGames()

        allGames: FrozenList[AbsTriviaGameState] = FrozenList()
        allGames.extend(normalGames)
        allGames.extend(superGames)
        allGames.freeze()

        return allGames

    async def getNormalGame(
        self,
        twitchChannelId: str,
        userId: str
    ) -> TriviaGameState | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        normalGames = await self.getNormalGames()

        for state in normalGames:
            if twitchChannelId == state.getTwitchChannelId() and userId == state.getUserId():
                return state

        return None

    async def getNormalGames(self) -> FrozenList[TriviaGameState]:
        frozenNormalGames: FrozenList[TriviaGameState] = FrozenList(self.__normalGameStates)
        frozenNormalGames.freeze()
        return frozenNormalGames

    async def getSuperGame(self, twitchChannelId: str) -> SuperTriviaGameState | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        superGames = await self.getSuperGames()

        for state in superGames:
            if twitchChannelId == state.getTwitchChannelId():
                return state

        return None

    async def getSuperGames(self) -> FrozenList[SuperTriviaGameState]:
        frozenSuperGames: FrozenList[SuperTriviaGameState] = FrozenList(self.__superGameStates)
        frozenSuperGames.freeze()
        return frozenSuperGames

    async def getTwitchChannelIdsWithActiveSuperGames(self) -> frozenset[str]:
        superGames = await self.getSuperGames()
        twitchChannelIds: set[str] = set()

        for state in superGames:
            twitchChannelIds.add(state.getTwitchChannelId())

        return frozenset(twitchChannelIds)

    async def removeNormalGame(
        self,
        twitchChannelId: str,
        userId: str
    ) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        normalGames = await self.getNormalGames()

        for index, state in enumerate(normalGames):
            if twitchChannelId == state.getTwitchChannelId() and userId == state.getUserId():
                del self.__normalGameStates[index]
                return True

        return False

    async def removeSuperGame(self, twitchChannelId: str) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        superGames = await self.getSuperGames()

        for index, state in enumerate(superGames):
            if twitchChannelId == state.getTwitchChannelId():
                del self.__superGameStates[index]
                return True

        return False
