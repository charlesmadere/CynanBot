import CynanBot.misc.utils as utils
from CynanBot.trivia.games.absTriviaGameState import AbsTriviaGameState
from CynanBot.trivia.games.superTriviaGameState import SuperTriviaGameState
from CynanBot.trivia.games.triviaGameState import TriviaGameState
from CynanBot.trivia.games.triviaGameStoreInterface import \
    TriviaGameStoreInterface
from CynanBot.trivia.games.triviaGameType import TriviaGameType
from CynanBot.trivia.triviaExceptions import UnknownTriviaGameTypeException


class TriviaGameStore(TriviaGameStoreInterface):

    def __init__(self):
        self.__normalGameStates: list[TriviaGameState] = list()
        self.__superGameStates: list[SuperTriviaGameState] = list()

    async def add(self, state: AbsTriviaGameState):
        if not isinstance(state, AbsTriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        if state.getTriviaGameType() is TriviaGameType.NORMAL:
            await self.__addNormalGame(state)
        elif state.getTriviaGameType() is TriviaGameType.SUPER:
            await self.__addSuperGame(state)
        else:
            raise UnknownTriviaGameTypeException(f'Unknown TriviaGameType: \"{state.getTriviaGameType()}\"')

    async def __addNormalGame(self, state: TriviaGameState):
        if not isinstance(state, TriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        self.__normalGameStates.append(state)

    async def __addSuperGame(self, state: SuperTriviaGameState):
        if not isinstance(state, SuperTriviaGameState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        self.__superGameStates.append(state)

    async def getAll(self) -> list[AbsTriviaGameState]:
        normalGames = await self.getNormalGames()
        superGames = await self.getSuperGames()

        allGames: list[AbsTriviaGameState] = list()
        allGames.extend(normalGames)
        allGames.extend(superGames)

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

    async def getNormalGames(self) -> list[TriviaGameState]:
        return utils.copyList(self.__normalGameStates)

    async def getSuperGame(self, twitchChannelId: str) -> SuperTriviaGameState | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        superGames = await self.getSuperGames()

        for state in superGames:
            if twitchChannelId == state.getTwitchChannelId():
                return state

        return None

    async def getSuperGames(self) -> list[SuperTriviaGameState]:
        return utils.copyList(self.__superGameStates)

    async def getTwitchChannelIdsWithActiveSuperGames(self) -> list[str]:
        superGames = await self.getSuperGames()
        twitchChannelIds: set[str] = set()

        for state in superGames:
            twitchChannelIds.add(state.getTwitchChannelId())

        return list(twitchChannelIds)

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
