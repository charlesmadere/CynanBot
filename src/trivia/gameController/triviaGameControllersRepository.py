from typing import Final

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class TriviaGameControllersRepository(TriviaGameControllersRepositoryInterface):

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
        self.__cache: Final[dict[str, frozenset[str] | None]] = dict()

    async def addController(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> AddTriviaGameControllerResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        currentControllers = await self.getControllers(
            twitchChannelId = twitchChannelId,
        )

        if userId in currentControllers:
            return AddTriviaGameControllerResult.ALREADY_EXISTS

        self.__cache.pop(twitchChannelId, None)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO triviagamecontrollers (twitchchannelid, userid)
                VALUES ($1, $2)
                ON CONFLICT (twitchchannelid, userid) DO NOTHING
            ''',
            twitchChannelId, userId
        )

        await connection.close()
        self.__timber.log('TriviaGameControllersRepository', f'Added a new trivia game controller ({twitchChannelId=}) ({userId=})')
        return AddTriviaGameControllerResult.ADDED

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TriviaGameControllersRepository', 'Caches cleared')

    async def getControllers(
        self,
        twitchChannelId: str,
    ) -> frozenset[str]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cachedControllers = self.__cache.get(twitchChannelId, None)

        if cachedControllers is not None:
            return cachedControllers

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT userid FROM triviagamecontrollers
                WHERE triviagamecontrollers.twitchchannelid = $1
            ''',
            twitchChannelId
        )

        await connection.close()
        controllers: set[str] = set()

        if records is not None and len(records) >= 1:
            for record in records:
                controllers.add(record[0])

        frozenControllers: frozenset[str] = frozenset(controllers)
        self.__cache[twitchChannelId] = frozenControllers
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
                        CREATE TABLE IF NOT EXISTS triviagamecontrollers (
                            twitchchannelid text NOT NULL,
                            userid text NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS triviagamecontrollers (
                            twitchchannelid TEXT NOT NULL,
                            userid TEXT NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def removeController(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> RemoveTriviaGameControllerResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        currentControllers = await self.getControllers(
            twitchChannelId = twitchChannelId,
        )

        if userId not in currentControllers:
            return RemoveTriviaGameControllerResult.DOES_NOT_EXIST

        self.__cache.pop(twitchChannelId, None)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM triviagamecontrollers
                WHERE twitchchannelid = $1 AND userid = $2
            ''',
            twitchChannelId, userId
        )

        await connection.close()
        self.__timber.log('TriviaGameControllersRepository', f'Finished removing trivia game controller ({twitchChannelId=}) ({userId=})')
        return RemoveTriviaGameControllerResult.REMOVED
