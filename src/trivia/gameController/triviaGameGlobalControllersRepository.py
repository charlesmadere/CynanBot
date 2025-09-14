from typing import Final

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameGlobalControllersRepositoryInterface import TriviaGameGlobalControllersRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class TriviaGameGlobalControllersRepository(TriviaGameGlobalControllersRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber

        self.__isDatabaseReady: bool = False
        self.__cache: frozenset[str] | None = None

    async def addController(
        self,
        userId: str,
    ) -> AddTriviaGameControllerResult:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        currentControllers = await self.getControllers()

        if userId in currentControllers:
            return AddTriviaGameControllerResult.ALREADY_EXISTS

        self.__cache = None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO triviagameglobalcontrollers (userid)
                VALUES ($1)
                ON CONFLICT (userid) DO NOTHING
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('TriviaGameGlobalControllersRepository', f'Added user to trivia game global controllers ({userId=})')
        return AddTriviaGameControllerResult.ADDED

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('TriviaGameGlobalControllersRepository', 'Caches cleared')

    async def getControllers(self) -> frozenset[str]:
        cachedControllers = self.__cache

        if cachedControllers is not None:
            return cachedControllers

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT userid FROM triviagameglobalcontrollers
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
                        CREATE TABLE IF NOT EXISTS triviagameglobalcontrollers (
                            userid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS triviagameglobalcontrollers (
                            userid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def removeController(
        self,
        userId: str,
    ) -> RemoveTriviaGameControllerResult:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        currentControllers = await self.getControllers()

        if userId not in currentControllers:
            return RemoveTriviaGameControllerResult.DOES_NOT_EXIST

        self.__cache = None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM triviagameglobalcontrollers
                WHERE userid = $1
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('TriviaGameGlobalControllersRepository', f'Removed user from trivia game global controllers ({userId=})')
        return RemoveTriviaGameControllerResult.REMOVED
