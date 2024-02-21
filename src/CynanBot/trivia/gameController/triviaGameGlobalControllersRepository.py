from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.gameController.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBot.trivia.gameController.triviaGameGlobalController import \
    TriviaGameGlobalController
from CynanBot.trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from CynanBot.trivia.gameController.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TriviaGameGlobalControllersRepository(TriviaGameGlobalControllersRepositoryInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(backingDatabase, BackingDatabase), f"malformed {backingDatabase=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False

    async def addController(self, userName: str) -> AddTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        administrator = await self.__administratorProvider.getAdministratorUserName()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(administrator)

        userId = await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(userId):
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to add \"{userName}\" as a trivia game global controller: \"{userId}\"')
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

        count: Optional[int] = None
        if utils.hasItems(record):
            count = record[0]

        if utils.isValidInt(count) and count >= 1:
            await connection.close()
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Tried to add userName=\"{userName}\" userId=\"{userId}\" as a trivia game global controller, but this user has already been added as one')
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
        self.__timber.log('TriviaGameGlobalControllersRepository', f'Added userName=\"{userName}\" userId=\"{userId}\" as a trivia game global controller')
        return AddTriviaGameControllerResult.ADDED

    async def getControllers(self) -> List[TriviaGameGlobalController]:
        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT triviagameglobalcontrollers.userid, userids.username FROM triviagameglobalcontrollers
                INNER JOIN userids ON triviagameglobalcontrollers.userid = userids.userid
                ORDER BY userids.username ASC
            '''
        )

        await connection.close()
        controllers: List[TriviaGameGlobalController] = list()

        if not utils.hasItems(records):
            return controllers

        for record in records:
            controllers.append(TriviaGameGlobalController(
                userId = record[0],
                userName = record[1]
            ))

        controllers.sort(key = lambda controller: controller.getUserName().lower())

        return controllers

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviagameglobalcontrollers (
                        userid public.citext NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviagameglobalcontrollers (
                        userid TEXT NOT NULL PRIMARY KEY COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def removeController(self, userName: str) -> RemoveTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        userId = await self.__userIdsRepository.fetchUserId(userName = userName)

        if not utils.isValidStr(userId):
            self.__timber.log('TriviaGameGlobalControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to remove \"{userName}\" as a trivia game global controller')
            return RemoveTriviaGameControllerResult.ERROR

        connection = await self.__backingDatabase.getConnection()
        await connection.execute(
            '''
                DELETE FROM triviagameglobalcontrollers
                WHERE userid = $1
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('TriviaGameGlobalControllersRepository', f'Removed userName=\"{userName}\" userId=\"{userId}\" as a trivia game global controller')

        return RemoveTriviaGameControllerResult.REMOVED
