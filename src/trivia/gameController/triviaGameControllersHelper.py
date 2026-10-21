import traceback
from typing import Collection, Final

from frozenlist import FrozenList

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .triviaGameControllersHelperInterface import TriviaGameControllersHelperInterface
from .triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from .triviaGameGlobalControllersRepositoryInterface import TriviaGameGlobalControllersRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...twitch.userIds.exceptions import NoTwitchUserDataFoundException
from ...twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class TriviaGameControllersHelper(TriviaGameControllersHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise TypeError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise TypeError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameControllersRepository: Final[TriviaGameControllersRepositoryInterface] = triviaGameControllersRepository
        self.__triviaGameGlobalControllersRepository: Final[TriviaGameGlobalControllersRepositoryInterface] = triviaGameGlobalControllersRepository
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

    async def addChannelController(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> TriviaGameControllersHelperInterface.AbsAddResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.__triviaGameControllersRepository.addController(
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        if result is AddTriviaGameControllerResult.ALREADY_EXISTS:
            return TriviaGameControllersHelperInterface.AlreadyExists()

        controllers = await self.__triviaGameControllersRepository.getControllers(
            twitchChannelId = twitchChannelId,
        )

        userData = await self.__twitchUserIdsHelper.requireById(
            userId = userId,
            twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
                twitchChannelId = twitchChannelId,
            ),
        )

        return TriviaGameControllersHelperInterface.Added(
            newTotal = len(controllers),
            userId = userData.getUserId(),
            userLogin = userData.getUserLogin(),
            userName = userData.getUserName(),
        )

    async def addGlobalController(
        self,
        userId: str,
    ) -> TriviaGameControllersHelperInterface.AbsAddResult:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.__triviaGameGlobalControllersRepository.addController(
            userId = userId,
        )

        if result is AddTriviaGameControllerResult.ALREADY_EXISTS:
            return TriviaGameControllersHelperInterface.AlreadyExists()

        controllers = await self.__triviaGameGlobalControllersRepository.getControllers()

        userData = await self.__twitchUserIdsHelper.requireById(
            userId = userId,
        )

        return TriviaGameControllersHelperInterface.Added(
            newTotal = len(controllers),
            userId = userData.getUserId(),
            userLogin = userData.getUserLogin(),
            userName = userData.getUserName(),
        )

    async def __buildControllersCollection(
        self,
        userIds: Collection[str],
        twitchAccessToken: str | None,
    ) -> Collection[TwitchUserInterface]:
        usersList: list[TwitchUserInterface] = list()

        for index, userId in enumerate(userIds):
            try:
                lookupUserData = await self.__twitchUserIdsHelper.requireById(
                    userId = userId,
                    twitchAccessToken = twitchAccessToken,
                )

                usersList.append(lookupUserData)
            except NoTwitchUserDataFoundException as e:
                self.__timber.log('TriviaGameControllersHelper', f'Failed to find user data for controller ({index=}) ({userId=})', e, traceback.format_exc())

        usersList.sort(key = lambda user: user.getUserName().casefold())
        frozenUsersList: FrozenList[TwitchUserInterface] = FrozenList(usersList)
        frozenUsersList.freeze()

        return frozenUsersList

    async def getChannelControllers(
        self,
        twitchChannelId: str,
    ) -> Collection[TwitchUserInterface]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        userIds = await self.__triviaGameControllersRepository.getControllers(
            twitchChannelId = twitchChannelId,
        )

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        return await self.__buildControllersCollection(
            userIds = userIds,
            twitchAccessToken = twitchAccessToken,
        )

    async def getGlobalControllers(self) -> Collection[TwitchUserInterface]:
        userIds = await self.__triviaGameGlobalControllersRepository.getControllers()

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle(),
        )

        return await self.__buildControllersCollection(
            userIds = userIds,
            twitchAccessToken = twitchAccessToken,
        )
