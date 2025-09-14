from typing import Final

from .addBannedTriviaGameControllerResult import AddBannedTriviaGameControllerResult
from .bannedTriviaGameControllersRepositoryInterface import BannedTriviaGameControllersRepositoryInterface
from .removeBannedTriviaGameControllerResult import RemoveBannedTriviaGameControllerResult
from ...misc import utils as utils
from ...misc.administratorProviderInterface import AdministratorProviderInterface
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class BannedTriviaGameControllersRepository(BannedTriviaGameControllersRepositoryInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber

        self.__isDatabaseReady: bool = False
        self.__cache: frozenset[str] | None = None

    async def addBannedController(
        self,
        userId: str,
    ) -> AddBannedTriviaGameControllerResult:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        if userId == await self.__administratorProvider.getAdministratorUserId():
            self.__timber.log('BannedTriviaGameControllersRepository', f'Tried to add banned trivia game controller, but this user is the administrator ({userId=})')
            return AddBannedTriviaGameControllerResult.ERROR

        bannedControllers = await self.getBannedControllers()

        if userId in bannedControllers:
            return AddBannedTriviaGameControllerResult.ALREADY_EXISTS

        self.__cache = None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO bannedtriviagamecontrollers (userid)
                VALUES ($1)
                ON CONFLICT (userid) DO NOTHING
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('BannedTriviaGameControllersRepository', f'Added banned trivia game controller ({userId=})')
        return AddBannedTriviaGameControllerResult.ADDED

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('BannedTriviaGameControllersRepository', 'Caches cleared')

    async def getBannedControllers(self) -> frozenset[str]:
        bannedControllers = self.__cache

        if bannedControllers is not None:
            return bannedControllers

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT userid FROM bannedtriviagamecontrollers
            '''
        )

        await connection.close()
        controllers: set[str] = set()

        if records is not None and len(records) >= 1:
            for record in records:
                controllers.add(record[0])

        frozenControllers: frozenset[str] = frozenset(controllers)
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
        userId: str,
    ) -> RemoveBannedTriviaGameControllerResult:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        bannedControllers = await self.getBannedControllers()

        if userId not in bannedControllers:
            return RemoveBannedTriviaGameControllerResult.NOT_BANNED

        self.__cache = None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM bannedtriviagamecontrollers
                WHERE userid = $1
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('BannedTriviaGameControllersRepository', f'Removed user from banned trivia game controllers ({userId=})')
        return RemoveBannedTriviaGameControllerResult.REMOVED
