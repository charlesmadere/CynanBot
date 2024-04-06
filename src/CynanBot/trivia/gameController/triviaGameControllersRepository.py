import traceback

import CynanBot.misc.utils as utils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.gameController.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBot.trivia.gameController.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult
from CynanBot.trivia.gameController.triviaGameController import \
    TriviaGameController
from CynanBot.trivia.gameController.triviaGameControllersRepositoryInterface import \
    TriviaGameControllersRepositoryInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TriviaGameControllersRepository(TriviaGameControllersRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False

    async def addController(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userName: str
    ) -> AddTriviaGameControllerResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchChannel)

        try:
            userId = await self.__userIdsRepository.requireUserId(
                userName = userName,
                twitchAccessToken = twitchAccessToken
            )
        except Exception as e:
            self.__timber.log('TriviaGameControllersRepository', f'Unable to find userId for \"{userName}\" when trying to add this user as a trivia game controller for \"{twitchChannel}\"', e, traceback.format_exc())
            return AddTriviaGameControllerResult.ERROR

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM triviagamecontrollers
                WHERE twitchchannel = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannel, userId
        )

        count: int | None = None
        if utils.hasItems(record):
            count = record[0]

        if utils.isValidInt(count) and count >= 1:
            await connection.close()
            self.__timber.log('TriviaGameControllersRepository', f'Tried to add {userName}:{userId} as a trivia game controller for \"{twitchChannel}\", but they\'ve already been added as one')
            return AddTriviaGameControllerResult.ALREADY_EXISTS

        await connection.execute(
            '''
                INSERT INTO triviagamecontrollers (twitchchannel, userid)
                VALUES ($1, $2)
                ON CONFLICT (twitchchannel, userid) DO NOTHING
            ''',
            twitchChannel, userId
        )

        await connection.close()
        self.__timber.log('TriviaGameControllersRepository', f'Added {userName}:{userId} as a trivia game controller for \"{twitchChannel}\"')
        return AddTriviaGameControllerResult.ADDED

    async def getControllers(self, twitchChannel: str, twitchChannelId: str) -> list[TriviaGameController]:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT triviagamecontrollers.twitchchannel, triviagamecontrollers.userid, userids.username FROM triviagamecontrollers
                INNER JOIN userids ON triviagamecontrollers.userid = userids.userid
                WHERE triviagamecontrollers.twitchchannel = $1
                ORDER BY userids.username ASC
            ''',
            twitchChannel
        )

        await connection.close()
        controllers: list[TriviaGameController] = list()

        if not utils.hasItems(records):
            return controllers

        for record in records:
            controllers.append(TriviaGameController(
                twitchChannel = record[0],
                userId = record[1],
                userName = record[2]
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
                    CREATE TABLE IF NOT EXISTS triviagamecontrollers (
                        twitchchannel public.citext NOT NULL,
                        userid public.citext NOT NULL,
                        PRIMARY KEY (twitchchannel, userid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviagamecontrollers (
                        twitchchannel TEXT NOT NULL COLLATE NOCASE,
                        userid TEXT NOT NULL COLLATE NOCASE,
                        PRIMARY KEY (twitchchannel, userid)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def removeController(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userName: str
    ) -> RemoveTriviaGameControllerResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        try:
            userId = await self.__userIdsRepository.requireUserId(userName = userName)
        except Exception as e:
            self.__timber.log('TriviaGameControllersRepository', f'Unable to find userId for \"{userName}\" when trying to remove this user as a trivia game controller for \"{twitchChannel}\"', e, traceback.format_exc())
            return RemoveTriviaGameControllerResult.ERROR

        connection = await self.__backingDatabase.getConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM triviagamecontrollers
                WHERE twitchchannel = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannel, userId
        )

        if record is None or len(record) < 1:
            await connection.close()
            self.__timber.log('TriviaGameControllersRepository', f'Tried to remove {userName}:{userId} as a trivia game controller from \"{twitchChannel}\", but they\'re not already added')
            return RemoveTriviaGameControllerResult.DOES_NOT_EXIST

        await connection.execute(
            '''
                DELETE FROM triviagamecontrollers
                WHERE twitchchannel = $1 AND userid = $2
            ''',
            twitchChannel, userId
        )

        await connection.close()
        self.__timber.log('TriviaGameControllersRepository', f'Removed {userName}:{userId} as a trivia game controller from \"{twitchChannel}\"')
        return RemoveTriviaGameControllerResult.REMOVED
