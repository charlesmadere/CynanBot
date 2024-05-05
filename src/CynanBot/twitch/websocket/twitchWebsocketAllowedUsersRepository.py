import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.websocket.twitchWebsocketAllowedUsersRepositoryInterface import \
    TwitchWebsocketAllowedUsersRepositoryInterface
from CynanBot.twitch.websocket.twitchWebsocketUser import TwitchWebsocketUser
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


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
        usersWithTwitchTokens: set[str]
    ) -> set[TwitchWebsocketUser]:
        users: set[TwitchWebsocketUser] = set()

        if len(usersWithTwitchTokens) == 0:
            return users

        for user in usersWithTwitchTokens:
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(user)

            if not utils.isValidStr(twitchAccessToken):
                self.__timber.log('TwitchWebsocketAllowedUsersRepository', f'Unable to find Twitch access token for \"{user}\"')
                continue

            userId = await self.__userIdsRepository.fetchUserId(
                userName = user,
                twitchAccessToken = twitchAccessToken
            )

            if not utils.isValidStr(userId):
                self.__timber.log('TwitchWebsocketAllowedUsersRepository', f'Unable to find user ID for \"{user}\" using Twitch access token \"{twitchAccessToken}\"')
                continue

            users.add(TwitchWebsocketUser(
                userId = userId,
                userName = user
            ))

        return users

    async def __findUsersWithTwitchTokens(self, enabledUsers: set[str]) -> set[str]:
        usersWithTwitchTokens: set[str] = set()

        if len(enabledUsers) == 0:
            return usersWithTwitchTokens

        for user in enabledUsers:
            if await self.__twitchTokensRepository.hasAccessToken(user):
                usersWithTwitchTokens.add(user)

        return usersWithTwitchTokens

    async def __getEnabledUsers(self) -> set[str]:
        enabledUsers: set[str] = set()
        users = await self.__usersRepository.getUsersAsync()

        for user in users:
            if user.isEnabled():
                enabledUsers.add(user.getHandle())

        return enabledUsers

    async def getUsers(self) -> set[TwitchWebsocketUser]:
        enabledUsers = await self.__getEnabledUsers()
        usersWithTwitchTokens = await self.__findUsersWithTwitchTokens(enabledUsers)
        users = await self.__buildTwitchWebsocketUsers(usersWithTwitchTokens)

        self.__timber.log('TwitchWebsocketAllowedUsersRepository', f'Built up a list of {len(users)} user(s) that are eligible for websocket connections')

        return users
 