from .twitchWebsocketAllowedUsersRepositoryInterface import TwitchWebsocketAllowedUsersRepositoryInterface
from .twitchWebsocketUser import TwitchWebsocketUser
from ..twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class TwitchWebsocketAllowedUsersRepository(TwitchWebsocketAllowedUsersRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __buildTwitchWebsocketUsers(
        self,
        userNamesWithTwitchTokens: set[str]
    ) -> set[TwitchWebsocketUser]:
        users: set[TwitchWebsocketUser] = set()

        if len(userNamesWithTwitchTokens) == 0:
            return users

        for userName in userNamesWithTwitchTokens:
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(userName)

            if not utils.isValidStr(twitchAccessToken):
                self.__timber.log('TwitchWebsocketAllowedUsersRepository', f'Unable to find Twitch access token for \"{userName}\"')
                continue

            userId = await self.__userIdsRepository.fetchUserId(
                userName = userName,
                twitchAccessToken = twitchAccessToken
            )

            if not utils.isValidStr(userId):
                self.__timber.log('TwitchWebsocketAllowedUsersRepository', f'Unable to find user ID for \"{userName}\" using Twitch access token \"{twitchAccessToken}\"')
                continue

            users.add(TwitchWebsocketUser(
                userId = userId,
                userName = userName
            ))

        return users

    async def __findUserNamesWithTwitchTokens(self, enabledUserNames: set[str]) -> set[str]:
        usersWithTwitchTokens: set[str] = set()

        if len(enabledUserNames) == 0:
            return usersWithTwitchTokens

        for userName in enabledUserNames:
            if await self.__twitchTokensRepository.hasAccessToken(userName):
                usersWithTwitchTokens.add(userName)

        return usersWithTwitchTokens

    async def __getEnabledUserNames(self) -> set[str]:
        enabledUsers: set[str] = set()
        users = await self.__usersRepository.getUsersAsync()

        for user in users:
            if user.isEnabled:
                enabledUsers.add(user.getHandle())

        return enabledUsers

    async def getUsers(self) -> set[TwitchWebsocketUser]:
        enabledUserNames = await self.__getEnabledUserNames()
        userNamesWithTwitchTokens = await self.__findUserNamesWithTwitchTokens(enabledUserNames)
        users = await self.__buildTwitchWebsocketUsers(userNamesWithTwitchTokens)

        self.__timber.log('TwitchWebsocketAllowedUsersRepository', f'Built up a list of {len(users)} user(s) that are eligible for websocket connections')

        return users
