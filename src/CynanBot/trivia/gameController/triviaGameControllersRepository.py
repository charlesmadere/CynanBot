from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.gameController.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBot.trivia.gameController.triviaGameController import \
    TriviaGameController
from CynanBot.trivia.gameController.triviaGameControllersRepositoryInterface import \
    TriviaGameControllersRepositoryInterface
from CynanBot.trivia.gameController.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult
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
        assert isinstance(backingDatabase, BackingDatabase), f"malformed {backingDatabase=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False

    async def addController(
        self,
        twitchChannel: str,
        userName: str
    ) -> AddTriviaGameControllerResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchChannel)

        userId = await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(userId):
            self.__timber.log('TriviaGameControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to add \"{userName}\" as a trivia game controller for \"{twitchChannel}\": \"{userId}\"')
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

        count: Optional[int] = None
        if utils.hasItems(record):
            count = record[0]

        if utils.isValidInt(count) and count >= 1:
            await connection.close()
            self.__timber.log('TriviaGameControllersRepository', f'Tried to add userName=\"{userName}\" userId=\"{userId}\" as a trivia game controller for \"{twitchChannel}\", but this user has already been added as one')
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
        self.__timber.log('TriviaGameControllersRepository', f'Added userName=\"{userName}\" userId=\"{userId}\" as a trivia game controller for \"{twitchChannel}\"')

        return AddTriviaGameControllerResult.ADDED

    async def getControllers(self, twitchChannel: str) -> List[TriviaGameController]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

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
        controllers: List[TriviaGameController] = list()

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
        userName: str
    ) -> RemoveTriviaGameControllerResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        userId = await self.__userIdsRepository.fetchUserId(userName = userName)

        if not utils.isValidStr(userId):
            self.__timber.log('TriviaGameControllersRepository', f'Retrieved no userId from UserIdsRepository when trying to remove \"{userName}\" as a trivia game controller for \"{twitchChannel}\"')
            return RemoveTriviaGameControllerResult.ERROR

        connection = await self.__backingDatabase.getConnection()
        await connection.execute(
            '''
                DELETE FROM triviagamecontrollers
                WHERE twitchchannel = $1 AND userid = $2
            ''',
            twitchChannel, userId
        )

        await connection.close()
        self.__timber.log('TriviaGameControllersRepository', f'Removed userName=\"{userName}\" userId=\"{userId}\" as a trivia game controller for \"{twitchChannel}\"')

        return RemoveTriviaGameControllerResult.REMOVED
