from __future__ import annotations

import traceback

from lru import LRU
from network.exceptions import GenericNetworkException
from storage.backingDatabase import BackingDatabase
from storage.databaseConnection import DatabaseConnection
from storage.databaseType import DatabaseType
from timber.timberInterface import TimberInterface
from twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from twitch.api.twitchUserDetails import TwitchUserDetails
from twitch.twitchAnonymousUserIdProviderInterface import \
    TwitchAnonymousUserIdProviderInterface
from users.exceptions import NoSuchUserException
from users.userIdsRepositoryInterface import UserIdsRepositoryInterface

from ..misc import utils as utils


class UserIdsRepository(UserIdsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        twitchAnonymousUserIdProvider: TwitchAnonymousUserIdProviderInterface,
        twitchApiService: TwitchApiServiceInterface,
        cacheSize: int = 256
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchAnonymousUserIdProvider, TwitchAnonymousUserIdProviderInterface):
            raise TypeError(f'twitchAnonymousUserIdProvider argument is malformed: \"{twitchAnonymousUserIdProvider}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__twitchAnonymousUserIdProvider: TwitchAnonymousUserIdProviderInterface = twitchAnonymousUserIdProvider
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService

        self.__isDatabaseReady: bool = False
        self.__cache: LRU[str, str | None] = LRU(cacheSize)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('UserIdsRepository', 'Caches cleared')

    async def fetchAnonymousUserId(self) -> str:
        return await self.__twitchAnonymousUserIdProvider.getTwitchAnonymousUserId()

    async def fetchAnonymousUserName(self, twitchAccessToken: str) -> str | None:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        anonymousUserId = await self.fetchAnonymousUserId()

        return await self.fetchUserName(
            userId = anonymousUserId,
            twitchAccessToken = twitchAccessToken
        )

    async def fetchUserId(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> str | None:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif twitchAccessToken is not None and not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT userid FROM userids
                WHERE username = $1
                LIMIT 1
            ''',
            userName
        )

        userId: str | None = None
        if record is not None and len(record) >= 1:
            userId = record[0]

        await connection.close()

        if utils.isValidStr(userId):
            return userId
        elif not utils.isValidStr(twitchAccessToken):
            self.__timber.log('UserIdsRepository', f'Can\'t lookup Twitch user ID for \"{userName}\" as no Twitch access token was specified')
            return None

        self.__timber.log('UserIdsRepository', f'User ID for username \"{userName}\" wasn\'t found locally, so performing a network call to fetch instead ({twitchAccessToken=})...')
        userDetails: TwitchUserDetails | None = None

        try:
            userDetails = await self.__twitchApiService.fetchUserDetailsWithUserName(
                twitchAccessToken = twitchAccessToken,
                userName = userName
            )
        except GenericNetworkException as e:
            self.__timber.log('UserIdsRepository', f'Received a network error when fetching Twitch user ID for username \"{userName}\" ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            return None

        if userDetails is None:
            self.__timber.log('UserIdsRepository', f'Unable to retrieve Twitch user ID for username \"{userName}\" ({twitchAccessToken=})')
            return None

        await self.setUser(
            userId = userDetails.userId,
            userName = userDetails.login
        )

        return userDetails.userId

    async def fetchUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> int | None:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif twitchAccessToken is not None and not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userId = await self.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(userId):
            return None

        try:
            return int(userId)
        except (SyntaxError, TypeError, ValueError) as e:
            self.__timber.log('UserIdsRepository', f'Encountered exception when attempting to convert userId (\"{userId}\") into int ({userName=}) ({twitchAccessToken=}): {e}')
            raise e

    async def fetchUserName(
        self,
        userId: str,
        twitchAccessToken: str | None = None
    ) -> str | None:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif twitchAccessToken is not None and not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userName: str | None = None

        if userId in self.__cache:
            userName = self.__cache[userId]

            if utils.isValidStr(userName):
                return userName

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT username FROM userids
                WHERE userid = $1
                LIMIT 1
            ''',
            userId
        )

        if record is not None and len(record) >= 1:
            userName = record[0]

        await connection.close()

        if utils.isValidStr(userName):
            self.__cache[userId] = userName
            return userName
        elif not utils.isValidStr(twitchAccessToken):
            self.__timber.log('UserIdsRepository', f'Can\'t lookup Twitch username for \"{userId}\" as no Twitch access token was specified')
            return None

        self.__timber.log('UserIdsRepository', f'Username for user ID \"{userId}\" wasn\'t found locally, so performing a network call to fetch instead ({twitchAccessToken=})...')
        userDetails: TwitchUserDetails | None = None

        try:
            userDetails = await self.__twitchApiService.fetchUserDetailsWithUserId(
                twitchAccessToken = twitchAccessToken,
                userId = userId
            )
        except GenericNetworkException as e:
            self.__timber.log('UserIdsRepository', f'Received a network error when fetching Twitch username for user ID \"{userId}\" ({twitchAccessToken=}): {e}', e, traceback.format_exc())
            return None

        if userDetails is None:
            self.__timber.log('UserIdsRepository', f'Unable to retrieve Twitch username for user ID \"{userId}\" ({twitchAccessToken=})')
            return None

        self.__cache[userId] = userDetails.login

        await self.setUser(
            userId = userId,
            userName = userDetails.login
        )

        return userDetails.login

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.getDatabaseType():
            case DatabaseType.POSTGRESQL:
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS userids (
                            userid text NOT NULL PRIMARY KEY,
                            username public.citext NOT NULL
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS userids (
                            userid TEXT NOT NULL PRIMARY KEY,
                            username TEXT NOT NULL COLLATE NOCASE
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def optionallySetUser(self, userId: str | None, userName: str | None):
        if utils.isValidStr(userId) and utils.isValidStr(userName):
            await self.setUser(userId = userId, userName = userName)

    async def requireAnonymousUserId(self) -> str:
        anonymousUserId = await self.fetchAnonymousUserId()

        if not utils.isValidStr(anonymousUserId):
            raise NoSuchUserException(f'Unable to fetch Twitch user ID for anonymous user')

        return anonymousUserId

    async def requireAnonymousUserName(self, twitchAccessToken: str) -> str:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        anonymousUserName = await self.fetchAnonymousUserName(twitchAccessToken)

        if not utils.isValidStr(anonymousUserName):
            raise NoSuchUserException(f'Unable to fetch Twitch user name for anonymous user')

        return anonymousUserName

    async def requireUserId(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> str:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif twitchAccessToken is not None and not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userId = await self.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(userId):
            raise NoSuchUserException(f'Unable to fetch Twitch user ID for username \"{userName}\" ({twitchAccessToken=})')

        return userId

    async def requireUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> int:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif twitchAccessToken is not None and not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userId = await self.fetchUserIdAsInt(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidInt(userId):
            raise NoSuchUserException(f'Unable to fetch Twitch user ID for username \"{userName}\" ({twitchAccessToken=})')

        return userId

    async def requireUserName(
        self,
        userId: str,
        twitchAccessToken: str | None = None
    ) -> str:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif twitchAccessToken is not None and not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')

        userName = await self.fetchUserName(
            userId = userId,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(userName):
            raise NoSuchUserException(f'Unable to fetch Twitch user name for user ID \"{userId}\" ({twitchAccessToken=})')

        return userName

    async def setUser(self, userId: str, userName: str):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO userids (userid, username)
                VALUES ($1, $2)
                ON CONFLICT (userid) DO UPDATE SET username = EXCLUDED.username
            ''',
            userId, userName
        )

        await connection.close()
        self.__cache[userId] = userName
