import traceback

from frozenlist import FrozenList

from .addBannedTriviaGameControllerResult import AddBannedTriviaGameControllerResult
from .bannedTriviaGameController import BannedTriviaGameController
from .bannedTriviaGameControllersRepositoryInterface import BannedTriviaGameControllersRepositoryInterface
from ..gameController.removeBannedTriviaGameControllerResult import RemoveBannedTriviaGameControllerResult
from ...misc import utils as utils
from ...misc.administratorProviderInterface import AdministratorProviderInterface
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class BannedTriviaGameControllersRepository(BannedTriviaGameControllersRepositoryInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False
        self.__cache: FrozenList[BannedTriviaGameController] | None = None

    async def addBannedController(
        self,
        userName: str
    ) -> AddBannedTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        administratorId = await self.__administratorProvider.getAdministratorUserId()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(administratorId)

        try:
            userId = await self.__userIdsRepository.fetchUserId(
                userName = userName,
                twitchAccessToken = twitchAccessToken
            )
        except Exception as e:
            self.__timber.log('BannedTriviaGameControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to add \"{userName}\" as a banned trivia game controller: {e}', e, traceback.format_exc())
            return AddBannedTriviaGameControllerResult.ERROR

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM bannedtriviagamecontrollers
                WHERE userid = $1
                LIMIT 1
            ''',
            userId
        )

        count: int | None = None
        if record is not None and len(record) >= 1:
            count = record[0]

        if utils.isValidInt(count) and count >= 1:
            await connection.close()
            self.__timber.log('BannedTriviaGameControllersRepository', f'Tried to add banned trivia game controller, but this user has already been banned ({userId=}) ({userName=})')
            return AddBannedTriviaGameControllerResult.ALREADY_EXISTS

        self.__cache = None

        await connection.execute(
            '''
                INSERT INTO bannedtriviagamecontrollers (userid)
                VALUES ($1)
                ON CONFLICT (userid) DO NOTHING
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('BannedTriviaGameControllersRepository', f'Added banned trivia game controller ({userId=}) ({userName=})')
        return AddBannedTriviaGameControllerResult.ADDED

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('BannedTriviaGameControllersRepository', 'Caches cleared')

    async def getBannedControllers(self) -> FrozenList[BannedTriviaGameController]:
        cachedControllers = self.__cache
        if cachedControllers is not None:
            return cachedControllers

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT bannedtriviagamecontrollers.userid, userids.username FROM bannedtriviagamecontrollers
                INNER JOIN userids ON bannedtriviagamecontrollers.userid = userids.userid
                ORDER BY userids.username ASC
            '''
        )

        await connection.close()

        controllers: list[BannedTriviaGameController] = list()

        if records is not None and len(records) >= 1:
            for record in records:
                controllers.append(BannedTriviaGameController(
                    userId = record[0],
                    userName = record[1]
                ))

            controllers.sort(key = lambda controller: controller.userName.casefold())

        frozenControllers: FrozenList[BannedTriviaGameController] = FrozenList(controllers)
        frozenControllers.freeze()
        self.__cache = frozenControllers

        return frozenControllers

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS bannedtriviagamecontrollers (
                            userid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS bannedtriviagamecontrollers (
                            userid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def removeBannedController(
        self,
        userName: str
    ) -> RemoveBannedTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        try:
            userId = await self.__userIdsRepository.requireUserId(userName = userName)
        except Exception as e:
            self.__timber.log('BannedTriviaGameControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to remove \"{userName}\" as a banned trivia game controller', e, traceback.format_exc())
            return RemoveBannedTriviaGameControllerResult.ERROR

        connection = await self.__backingDatabase.getConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM bannedtriviagamecontrollers
                WHERE userid = $1
                LIMIT 1
            ''',
            userId
        )

        count: int | None = None
        if record is not None and len(record) >= 1:
            count = record[0]

        if not utils.isValidInt(count) or count < 1:
            await connection.close()
            self.__timber.log('BannedTriviaGameControllersRepository', f'Tried to removed banned trivia game controller, but this user has not already been banned ({userId=}) ({userName=})')
            return RemoveBannedTriviaGameControllerResult.NOT_BANNED

        self.__cache = None

        await connection.execute(
            '''
                DELETE FROM bannedtriviagamecontrollers
                WHERE userid = $1
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('BannedTriviaGameControllersRepository', f'Removed banned trivia game controller ({userId=}) ({userName=})')
        return RemoveBannedTriviaGameControllerResult.REMOVED
