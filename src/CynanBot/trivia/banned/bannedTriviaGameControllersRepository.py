import traceback

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

    async def addBannedController(self, userName: str) -> AddBannedTriviaGameControllerResult:
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        administrator = await self.__administratorProvider.getAdministratorUserName()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(administrator)

        try:
            userId = await self.__userIdsRepository.fetchUserId(
                userName = userName,
                twitchAccessToken = twitchAccessToken
            )
        except Exception as e:
            self.__timber.log('BannedTriviaGameControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to add \"{userName}\" as a banned trivia game controller', e, traceback.format_exc())
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

    async def getBannedControllers(self) -> list[BannedTriviaGameController]:
        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT bannedtriviagamecontrollers.userid, userids.username FROM bannedtriviagamecontrollers
                INNER JOIN userids ON bannedtriviagamecontrollers.userid = userids.userid
                ORDER BY userids.username ASC
            '''
        )

        controllers: list[BannedTriviaGameController] = list()

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
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        try:
            userId = await self.__userIdsRepository.requireUserId(userName = userName)
        except Exception as e:
            self.__timber.log('BannedTriviaGameControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to remove \"{userName}\" as a banned trivia game controller', e, traceback.format_exc())
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
