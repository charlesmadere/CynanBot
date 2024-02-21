from typing import List, Optional, Set

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
        self.__normalGameStates: List[TriviaGameState] = list()
        self.__superGameStates: List[SuperTriviaGameState] = list()

    async def add(self, state: AbsTriviaGameState):
        assert isinstance(state, AbsTriviaGameState), f"malformed {state=}"

        if state.getTriviaGameType() is TriviaGameType.NORMAL:
            await self.__addNormalGame(state)
        elif state.getTriviaGameType() is TriviaGameType.SUPER:
            await self.__addSuperGame(state)
        else:
            raise UnknownTriviaGameTypeException(f'Unknown TriviaGameType: \"{state.getTriviaGameType()}\"')

    async def __addNormalGame(self, state: TriviaGameState):
        assert isinstance(state, TriviaGameState), f"malformed {state=}"

        self.__normalGameStates.append(state)

    async def __addSuperGame(self, state: SuperTriviaGameState):
        assert isinstance(state, SuperTriviaGameState), f"malformed {state=}"

        self.__superGameStates.append(state)

    async def getAll(self) -> List[AbsTriviaGameState]:
        normalGames = await self.getNormalGames()
        superGames = await self.getSuperGames()

        allGames: List[AbsTriviaGameState] = list()
        allGames.extend(normalGames)
        allGames.extend(superGames)

        return allGames

    async def getNormalGame(self, twitchChannel: str, userId: str) -> Optional[TriviaGameState]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        normalGames = await self.getNormalGames()
        twitchChannel = twitchChannel.lower()
        userId = userId.lower()

        for state in normalGames:
            if twitchChannel == state.getTwitchChannel().lower() and userId == state.getUserId().lower():
                return state

        return None

    async def getNormalGames(self) -> List[TriviaGameState]:
        return utils.copyList(self.__normalGameStates)

    async def getSuperGame(self, twitchChannel: str) -> Optional[SuperTriviaGameState]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        superGames = await self.getSuperGames()
        twitchChannel = twitchChannel.lower()

        for state in superGames:
            if twitchChannel == state.getTwitchChannel().lower():
                return state

        return None

    async def getSuperGames(self) -> List[SuperTriviaGameState]:
        return utils.copyList(self.__superGameStates)

    async def getTwitchChannelsWithActiveSuperGames(self) -> List[str]:
        superGames = await self.getSuperGames()
        twitchChannels: Set[str] = set()

        for state in superGames:
            twitchChannels.add(state.getTwitchChannel().lower())

        return list(twitchChannels)

    async def removeNormalGame(self, twitchChannel: str, userId: str) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        normalGames = await self.getNormalGames()
        twitchChannel = twitchChannel.lower()
        userId = userId.lower()

        for index, state in enumerate(normalGames):
            if twitchChannel == state.getTwitchChannel().lower() and userId == state.getUserId().lower():
                del self.__normalGameStates[index]
                return True

        return False

    async def removeSuperGame(self, twitchChannel: str) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        superGames = await self.getSuperGames()
        twitchChannel = twitchChannel.lower()

        for index, state in enumerate(superGames):
            if twitchChannel == state.getTwitchChannel().lower():
                del self.__superGameStates[index]
                return True

        return False
