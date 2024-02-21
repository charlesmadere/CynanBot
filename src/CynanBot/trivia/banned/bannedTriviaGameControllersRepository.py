from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.banned.addBannedTriviaGameControllerResult import \
    AddBannedTriviaGameControllerResult
from CynanBot.trivia.banned.bannedTriviaGameController import \
    BannedTriviaGameController
from CynanBot.trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from CynanBot.trivia.gameController.removeBannedTriviaGameControllerResult import \
    RemoveBannedTriviaGameControllerResult
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class BannedTriviaGameControllersRepository(BannedTriviaGameControllersRepositoryInterface):

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

    async def addBannedController(self, userName: str) -> AddBannedTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        administrator = await self.__administratorProvider.getAdministratorUserName()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(administrator)

        userId = await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(userId):
            self.__timber.log('BannedTriviaGameControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to add \"{userName}\" as a banned trivia game controller: \"{userId}\"')
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

        count: Optional[int] = None
        if utils.hasItems(record):
            count = record[0]

        if utils.isValidInt(count) and count >= 1:
            await connection.close()
            self.__timber.log('BannedTriviaGameControllersRepository', f'Tried to add userName=\"{userName}\" userId=\"{userId}\" as a banned trivia game controller, but this user has already been added as one')
            return AddBannedTriviaGameControllerResult.ALREADY_EXISTS

        await connection.execute(
            '''
                INSERT INTO bannedtriviagamecontrollers (userid)
                VALUES ($1)
                ON CONFLICT (userid) DO NOTHING
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('BannedTriviaGameControllersRepository', f'Added userName=\"{userName}\" userId=\"{userId}\" as a banned trivia game controller')

        return AddBannedTriviaGameControllerResult.ADDED

    async def getBannedControllers(self) -> List[BannedTriviaGameController]:
        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT bannedtriviagamecontrollers.userid, userids.username FROM bannedtriviagamecontrollers
                INNER JOIN userids ON bannedtriviagamecontrollers.userid = userids.userid
                ORDER BY userids.username ASC
            '''
        )

        controllers: List[BannedTriviaGameController] = list()

        if not utils.hasItems(records):
            await connection.close()
            return controllers

        for record in records:
            controllers.append(BannedTriviaGameController(
                userId = record[0],
                userName = record[1]
            ))

        await connection.close()
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
                    CREATE TABLE IF NOT EXISTS bannedtriviagamecontrollers (
                        userid public.citext NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS bannedtriviagamecontrollers (
                        userid TEXT NOT NULL PRIMARY KEY COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def removeBannedController(self, userName: str) -> RemoveBannedTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        userId = await self.__userIdsRepository.fetchUserId(userName = userName)

        if not utils.isValidStr(userId):
            self.__timber.log('BannedTriviaGameControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to remove \"{userName}\" as a banned trivia game controller')
            return RemoveBannedTriviaGameControllerResult.ERROR

        connection = await self.__backingDatabase.getConnection()
        await connection.execute(
            '''
                DELETE FROM bannedtriviagamecontrollers
                WHERE userid = $1
            ''',
            userId
        )

        await connection.close()
        self.__timber.log('BannedTriviaGameControllersRepository', f'Removed userName=\"{userName}\" userId=\"{userId}\" as a banned trivia game controller')

        return RemoveBannedTriviaGameControllerResult.REMOVED
