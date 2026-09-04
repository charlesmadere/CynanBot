from datetime import datetime
from typing import Collection, Final

from lru import LRU

from .exceptions import NoTwitchUserDataFoundException
from .twitchUserData import TwitchUserData
from .twitchUserIdsRepositoryInterface import TwitchUserIdsRepositoryInterface
from .twitchUserStub import TwitchUserStub
from ..localModels.twitchUserInterface import TwitchUserInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class TwitchUserIdsRepository(TwitchUserIdsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cacheSize: int = 1024,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 16 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False
        self.__cache: Final[LRU[str, TwitchUserData | None]] = LRU(cacheSize)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchUserIdsRepository', 'Caches cleared')

    async def getById(
        self,
        userId: str,
    ) -> TwitchUserData | None:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        if userId in self.__cache:
            return self.__cache.get(userId, None)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT storedatetime, userlogin, username
                FROM twitchuserids
                WHERE userid = $1
                LIMIT 1
            ''',
            userId,
        )

        userData: TwitchUserData | None = None

        if record is not None and len(record) >= 1:
            userData = TwitchUserData(
                storeDateTime = datetime.fromisoformat(record[0]),
                userId = userId,
                userLogin = record[1],
                userName = record[2],
            )

        await connection.close()
        self.__cache[userId] = userData
        return userData

    async def getByLoginOrName(
        self,
        userLoginOrName: str,
    ) -> TwitchUserData | None:
        if not utils.isValidStr(userLoginOrName):
            raise TypeError(f'userLoginOrName argument is malformed: \"{userLoginOrName}\"')

        connection = await self.__getDatabaseConnection()

        userData = await self.__getByLogin(
            connection = connection,
            userLogin = userLoginOrName,
        )

        if userData is None:
            userData = await self.__getByName(
                connection = connection,
                userName = userLoginOrName,
            )

        await connection.close()

        if userData is not None:
            self.__cache[userData.userId] = userData

        return userData

    async def __getByLogin(
        self,
        connection: DatabaseConnection,
        userLogin: str,
    ) -> TwitchUserData | None:
        record = await connection.fetchRow(
            '''
                SELECT storedatetime, userid, userlogin, username
                FROM twitchuserids
                WHERE userlogin = $1
                LIMIT 1
            ''',
            userLogin,
        )

        if record is not None and len(record) >= 1:
            return TwitchUserData(
                storeDateTime = datetime.fromisoformat(record[0]),
                userId = record[1],
                userLogin = record[2],
                userName = record[3],
            )
        else:
            return None

    async def __getByName(
        self,
        connection: DatabaseConnection,
        userName: str,
    ) -> TwitchUserData | None:
        record = await connection.fetchRow(
            '''
                SELECT storedatetime, userid, userlogin, username
                FROM twitchuserids
                WHERE username = $1
                LIMIT 1
            ''',
            userName,
        )

        if record is not None and len(record) >= 1:
            return TwitchUserData(
                storeDateTime = datetime.fromisoformat(record[0]),
                userId = record[1],
                userLogin = record[2],
                userName = record[3],
            )
        else:
            return None

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getIdByLoginOrName(
        self,
        userLoginOrName: str,
    ) -> str | None:
        if not utils.isValidStr(userLoginOrName):
            raise TypeError(f'userLoginOrName argument is malformed: \"{userLoginOrName}\"')

        userData = await self.getByLoginOrName(
            userLoginOrName = userLoginOrName,
        )

        if userData is None:
            return None

        return userData.userId

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS twitchuserids (
                            storedatetime text NOT NULL,
                            userid text NOT NULL PRIMARY KEY,
                            userlogin public.citext NOT NULL,
                            username public.citext NOT NULL
                        )
                    ''',
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS twitchuserids (
                            storedatetime TEXT NOT NULL,
                            userid TEXT NOT NULL PRIMARY KEY,
                            userlogin TEXT NOT NULL COLLATE NOCASE,
                            username TEXT NOT NULL COLLATE NOCASE
                        ) STRICT
                    ''',
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def requireById(
        self,
        userId: str,
    ) -> TwitchUserData:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        userData = await self.getById(
            userId = userId,
        )

        if userData is None:
            raise NoTwitchUserDataFoundException(f'No Twitch user data found for userId: \"{userId}\"')

        return userData

    async def requireByLoginOrName(
        self,
        userLoginOrName: str,
    ) -> TwitchUserData:
        if not utils.isValidStr(userLoginOrName):
            raise TypeError(f'userLoginOrName argument is malformed: \"{userLoginOrName}\"')

        userData = await self.getByLoginOrName(
            userLoginOrName = userLoginOrName,
        )

        if userData is None:
            raise NoTwitchUserDataFoundException(f'No Twitch user data found for userLoginOrName: \"{userLoginOrName}\"')

        return userData

    async def requireIdByLoginOrName(
        self,
        userLoginOrName: str,
    ) -> str:
        if not utils.isValidStr(userLoginOrName):
            raise TypeError(f'userLoginOrName argument is malformed: \"{userLoginOrName}\"')

        userData = await self.getByLoginOrName(
            userLoginOrName = userLoginOrName,
        )

        if userData is None:
            raise NoTwitchUserDataFoundException(f'No Twitch user data found for userLoginOrName: \"{userLoginOrName}\"')

        return userData.userId

    async def set(
        self,
        userId: str,
        userLogin: str,
        userName: str,
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        userStubs: Collection[TwitchUserStub] = frozenset({
            TwitchUserStub(
                userId = userId,
                userLogin = userLogin,
                userName = userName,
            ),
        })

        await self.setAll(
            userStubs = userStubs,
        )

    async def setAll(
        self,
        userStubs: Collection[TwitchUserInterface],
    ):
        if not isinstance(userStubs, Collection):
            raise TypeError(f'userStubs argument is malformed: \"{userStubs}\"')

        storeDateTime = self.__timeZoneRepository.getNow()
        connection = await self.__getDatabaseConnection()

        for user in userStubs:
            await connection.execute(
                '''
                    INSERT INTO twitchuserids (storedatetime, userid, userlogin, username)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (userid) DO UPDATE SET storedatetime = EXCLUDED.storedatetime, userlogin = EXCLUDED.userlogin, username = EXCLUDED.username
                ''',
                storeDateTime.isoformat(), user.getUserId(), user.getUserLogin(), user.getUserName(),
            )

            self.__cache[user.getUserId()] = TwitchUserData(
                storeDateTime = storeDateTime,
                userId = user.getUserId(),
                userLogin = user.getUserLogin(),
                userName = user.getUserName(),
            )

        await connection.close()
