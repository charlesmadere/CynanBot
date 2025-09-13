import traceback
from typing import Final

from frozenlist import FrozenList

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameGlobalController import TriviaGameGlobalController
from .triviaGameGlobalControllersRepositoryInterface import TriviaGameGlobalControllersRepositoryInterface
from ...misc import utils as utils
from ...misc.administratorProviderInterface import AdministratorProviderInterface
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
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

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__isDatabaseReady: bool = False
        self.__cache: FrozenList[TriviaGameGlobalController] | None = None

    async def addController(
        self,
        userName: str,
    ) -> AddTriviaGameControllerResult:
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

        currentControllers = await self.getControllers()
        isCurrentController = False

        for currentController in currentControllers:
            if currentController.userId == userId:
                isCurrentController = True
                break

        if isCurrentController:
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Tried to add user to trivia game global controllers, but this user has already been added as one ({userName=}) ({userId=})')
            return AddTriviaGameControllerResult.ALREADY_EXISTS

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
        self.__cache = None
        self.__timber.log('TriviaGameGlobalControllersRepository', f'Added user to trivia game global controllers ({userName=}) ({userId=})')

        return AddTriviaGameControllerResult.ADDED

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('TriviaGameGlobalControllersRepository', 'Caches cleared')

    async def getControllers(self) -> FrozenList[TriviaGameGlobalController]:
        cachedControllers = self.__cache
        if cachedControllers is not None:
            return cachedControllers

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

        if records is not None and len(records) >= 1:
            for record in records:
                controllers.append(TriviaGameGlobalController(
                    userId = record[0],
                    userName = record[1]
                ))

            controllers.sort(key = lambda controller: controller.userName.casefold())

        frozenControllers: FrozenList[TriviaGameGlobalController] = FrozenList(controllers)
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
        userName: str
    ) -> RemoveTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        try:
            userId = await self.__userIdsRepository.requireUserId(userName = userName)
        except Exception as e:
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Unable to find userId when trying to remove user as a trivia game global controller ({userName=}): {e}', e, traceback.format_exc())
            return RemoveTriviaGameControllerResult.ERROR

        currentControllers = await self.getControllers()
        isCurrentController = False

        for currentController in currentControllers:
            if currentController.userId == userId:
                isCurrentController = True
                break

        if not isCurrentController:
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Tried to remove trivia game global controller, but they\'re not already added as one ({userName=}) ({userId=})')
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
        self.__cache = None
        self.__timber.log('TriviaGameGlobalControllersRepository', f'Removed user from trivia game global controllers ({userName=}) ({userId=})')

        return RemoveTriviaGameControllerResult.REMOVED
