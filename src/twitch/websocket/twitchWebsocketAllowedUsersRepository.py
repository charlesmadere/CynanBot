from typing import Final

from .twitchWebsocketAllowedUsersRepositoryInterface import TwitchWebsocketAllowedUsersRepositoryInterface
from .twitchWebsocketUser import TwitchWebsocketUser
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchWebsocketAllowedUsersRepository(TwitchWebsocketAllowedUsersRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def __buildTwitchWebsocketUsers(
        self,
        enabledUserNames: set[str],
    ) -> set[TwitchWebsocketUser]:
        users: set[TwitchWebsocketUser] = set()

        if len(enabledUserNames) == 0:
            return users

        for index, userName in enumerate(enabledUserNames):
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(
                twitchChannel = userName,
            )

            if not utils.isValidStr(twitchAccessToken):
                continue

            userData = await self.__twitchUserIdsHelper.getByLoginOrName(
                userLoginOrName = userName,
                twitchAccessToken = twitchAccessToken,
            )

            if userData is None:
                self.__timber.log('TwitchWebsocketAllowedUsersRepository', f'Unable to find user data when building up Twitch Websocket user list ({userName=}) ({index=}) ({userData=})')
                continue

            users.add(TwitchWebsocketUser(
                userId = userData.userId,
                userLogin = userData.userLogin,
                userName = userData.userName,
            ))

        return users

    async def __getEnabledUserNames(self) -> set[str]:
        enabledUsers: set[str] = set()
        users = await self.__usersRepository.getUsersAsync()

        for user in users:
            if user.isEnabled:
                enabledUsers.add(user.handle)

        return enabledUsers

    async def getUsers(self) -> frozenset[TwitchWebsocketUser]:
        enabledUserNames = await self.__getEnabledUserNames()
        users = await self.__buildTwitchWebsocketUsers(enabledUserNames)

        self.__timber.log('TwitchWebsocketAllowedUsersRepository', f'Built up a list of {len(users)} user(s) that are eligible for websocket connections')

        return frozenset(users)
