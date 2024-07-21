import traceback

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameGlobalController import TriviaGameGlobalController
from .triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from ...misc import utils as utils
from ...misc.administratorProviderInterface import AdministratorProviderInterface
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface
from ...twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TriviaGameGlobalControllersRepository(TriviaGameGlobalControllersRepositoryInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False

    async def addController(self, userName: str) -> AddTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        administratorId = await self.__administratorProvider.getAdministratorUserId()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(administratorId)

        try:
            userId = await self.__userIdsRepository.requireUserId(
                userName = userName,
                twitchAccessToken = twitchAccessToken
            )
        except Exception as e:
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Unable to find userId when trying to add a trivia game global controller ({userName=}): {e}', e, traceback.format_exc())
            return AddTriviaGameControllerResult.ERROR

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM triviagameglobalcontrollers
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
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Tried to add user to trivia game global controllers, but this user has already been added as one ({userName=}) ({userId=})')
            return AddTriviaGameControllerResult.ALREADY_EXISTS

        await connection.execute(
            '''
                INSERT INTO triviagameglobalcontrollers (userid)
                VALUES ($1)
                ON CONFLICT (userid) DO NOTHING
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('TriviaGameGlobalControllersRepository', f'Added user to trivia game global controllers ({userName=}) ({userId=})')
        return AddTriviaGameControllerResult.ADDED

    async def getControllers(self) -> list[TriviaGameGlobalController]:
        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT triviagameglobalcontrollers.userid, userids.username FROM triviagameglobalcontrollers
                INNER JOIN userids ON triviagameglobalcontrollers.userid = userids.userid
                ORDER BY userids.username ASC
            '''
        )

        await connection.close()
        controllers: list[TriviaGameGlobalController] = list()

        if records is None or len(records) == 0:
            return controllers

        for record in records:
            controllers.append(TriviaGameGlobalController(
                userId = record[0],
                userName = record[1]
            ))

        controllers.sort(key = lambda controller: controller.userName.casefold())
        return controllers

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
                        CREATE TABLE IF NOT EXISTS triviagameglobalcontrollers (
                            userid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS triviagameglobalcontrollers (
                            userid TEXT NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def removeController(self, userName: str) -> RemoveTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        try:
            userId = await self.__userIdsRepository.requireUserId(userName = userName)
        except Exception as e:
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Unable to find userId when trying to remove user as a trivia game global controller ({userName=}): {e}', e, traceback.format_exc())
            return RemoveTriviaGameControllerResult.ERROR

        connection = await self.__backingDatabase.getConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM triviagameglobalcontrollers
                WHERE userid = $1
                LIMIT 1
            ''',
            userId
        )

        if record is None or len(record) < 1:
            await connection.close()
            self.__timber.log('TriviaGameControllersRepository', f'Tried to remove trivia game global controller, but they\'re not already added ({userName=}) ({userId=})')
            return RemoveTriviaGameControllerResult.DOES_NOT_EXIST

        connection = await self.__backingDatabase.getConnection()
        await connection.execute(
            '''
                DELETE FROM triviagameglobalcontrollers
                WHERE userid = $1
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('TriviaGameGlobalControllersRepository', f'Removed user from trivia game global controllers ({userName=}) ({userId=})')
        return RemoveTriviaGameControllerResult.REMOVED
