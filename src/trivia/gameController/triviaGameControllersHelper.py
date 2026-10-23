import traceback
from typing import Collection, Final

from frozenlist import FrozenList

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .exceptions import TriviaGameControllerAlreadyExistsException
from .triviaGameControllersHelperInterface import TriviaGameControllersHelperInterface
from .triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from .triviaGameGlobalControllersRepositoryInterface import TriviaGameGlobalControllersRepositoryInterface
from ..banned.addBannedTriviaGameControllerResult import AddBannedTriviaGameControllerResult
from ..banned.bannedTriviaGameControllersRepositoryInterface import BannedTriviaGameControllersRepositoryInterface
from ...misc import utils as utils
from ...misc.administratorProviderInterface import AdministratorProviderInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...twitch.userIds.exceptions import NoTwitchUserDataFoundException
from ...twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class TriviaGameControllersHelper(TriviaGameControllersHelperInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
        elif not isinstance(timber, TimberInterface):
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

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__bannedTriviaGameControllersRepository: Final[BannedTriviaGameControllersRepositoryInterface] = bannedTriviaGameControllersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameControllersRepository: Final[TriviaGameControllersRepositoryInterface] = triviaGameControllersRepository
        self.__triviaGameGlobalControllersRepository: Final[TriviaGameGlobalControllersRepositoryInterface] = triviaGameGlobalControllersRepository
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

    async def addBannedController(
        self,
        userId: str,
    ) -> TriviaGameControllersHelperInterface.AddedResult:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.__bannedTriviaGameControllersRepository.addBannedController(
            userId = userId,
        )

        if result is AddBannedTriviaGameControllerResult.ALREADY_EXISTS:
            raise TriviaGameControllerAlreadyExistsException(f'This banned trivia game controller was already added ({userId=})')

        controllers = await self.__bannedTriviaGameControllersRepository.getBannedControllers()

        userData = await self.__twitchUserIdsHelper.requireById(
            userId = userId,
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
                twitchChannel = await self.__twitchHandleProvider.getTwitchHandle(),
            ),
        )

        return TriviaGameControllersHelperInterface.AddedResult(
            newTotal = len(controllers),
            userId = userData.getUserId(),
            userLogin = userData.getUserLogin(),
            userName = userData.getUserName(),
        )

    async def addChannelController(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> TriviaGameControllersHelperInterface.AddedResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.__triviaGameControllersRepository.addController(
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        if result is AddTriviaGameControllerResult.ALREADY_EXISTS:
            raise TriviaGameControllerAlreadyExistsException(f'This trivia game channel controller was already added ({twitchChannelId=}) ({userId=})')

        controllers = await self.__triviaGameControllersRepository.getControllers(
            twitchChannelId = twitchChannelId,
        )

        userData = await self.__twitchUserIdsHelper.requireById(
            userId = userId,
            twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
                twitchChannelId = twitchChannelId,
            ),
        )

        return TriviaGameControllersHelperInterface.AddedResult(
            newTotal = len(controllers),
            userId = userData.getUserId(),
            userLogin = userData.getUserLogin(),
            userName = userData.getUserName(),
        )

    async def addGlobalController(
        self,
        userId: str,
    ) -> TriviaGameControllersHelperInterface.AddedResult:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.__triviaGameGlobalControllersRepository.addController(
            userId = userId,
        )

        if result is AddTriviaGameControllerResult.ALREADY_EXISTS:
            raise TriviaGameControllerAlreadyExistsException(f'This trivia game global controller was already added ({userId=})')

        controllers = await self.__triviaGameGlobalControllersRepository.getControllers()

        userData = await self.__twitchUserIdsHelper.requireById(
            userId = userId,
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
                twitchChannel = await self.__twitchHandleProvider.getTwitchHandle(),
            ),
        )

        return TriviaGameControllersHelperInterface.AddedResult(
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

    async def getAllLocallyAuthorizedControllerIds(
        self,
        twitchChannelId: str,
    ) -> Collection[str]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        administratorUserId = await self.__administratorProvider.getAdministratorUserId()

        channelControllers = await self.__triviaGameControllersRepository.getControllers(
            twitchChannelId = twitchChannelId,
        )

        globalControllers = await self.__triviaGameGlobalControllersRepository.getControllers()

        bannedControllers = await self.__bannedTriviaGameControllersRepository.getBannedControllers()

        locallyAuthorizedControllers: set[str] = set()
        locallyAuthorizedControllers.add(twitchChannelId)
        locallyAuthorizedControllers.add(administratorUserId)
        locallyAuthorizedControllers.update(channelControllers)
        locallyAuthorizedControllers.update(globalControllers)
        locallyAuthorizedControllers.difference_update(bannedControllers)
        return frozenset(locallyAuthorizedControllers)

    async def getBannedControllers(self) -> Collection[TwitchUserInterface]:
        userIds = await self.__bannedTriviaGameControllersRepository.getBannedControllers()

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle(),
        )

        return await self.__buildControllersCollection(
            userIds = userIds,
            twitchAccessToken = twitchAccessToken,
        )

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
