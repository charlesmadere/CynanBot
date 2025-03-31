import traceback

from frozenlist import FrozenList

from .addTriviaGameControllerResult import AddTriviaGameControllerResult
from .removeTriviaGameControllerResult import RemoveTriviaGameControllerResult
from .triviaGameController import TriviaGameController
from .triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


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
        self.__cache: dict[str, FrozenList[TriviaGameController] | None] = dict()

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

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(twitchChannelId)

        try:
            userId = await self.__userIdsRepository.requireUserId(
                userName = userName,
                twitchAccessToken = twitchAccessToken
            )
        except Exception as e:
            self.__timber.log('TriviaGameControllersRepository', f'Unable to find userId when trying to add a trivia game controller ({twitchChannelId=}) ({userName=}): {e}', e, traceback.format_exc())
            return AddTriviaGameControllerResult.ERROR

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM triviagamecontrollers
                WHERE twitchchannelid = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannelId, userId
        )

        count: int | None = None
        if record is not None and len(record) >= 1:
            count = record[0]

        if utils.isValidInt(count) and count >= 1:
            await connection.close()
            self.__timber.log('TriviaGameControllersRepository', f'Tried to add a trivia game controller, but this user has already been added ({twitchChannelId=}) ({userName=}) ({userId=})')
            return AddTriviaGameControllerResult.ALREADY_EXISTS

        self.__cache.pop(twitchChannelId, None)

        await connection.execute(
            '''
                INSERT INTO triviagamecontrollers (twitchchannelid, userid)
                VALUES ($1, $2)
                ON CONFLICT (twitchchannelid, userid) DO NOTHING
            ''',
            twitchChannelId, userId
        )

        await connection.close()
        self.__timber.log('TriviaGameControllersRepository', f'Added a new trivia game controller ({twitchChannelId=}) ({userName=}) ({userId=})')
        return AddTriviaGameControllerResult.ADDED

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TriviaGameControllersRepository', 'Caches cleared')

    async def getControllers(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> FrozenList[TriviaGameController]:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cachedControllers = self.__cache.get(twitchChannelId, None)
        if cachedControllers is not None:
            return cachedControllers

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT triviagamecontrollers.twitchchannelid, triviagamecontrollers.userid, userids.username FROM triviagamecontrollers
                INNER JOIN userids ON triviagamecontrollers.userid = userids.userid
                WHERE triviagamecontrollers.twitchchannelid = $1
                ORDER BY userids.username ASC
            ''',
            twitchChannelId
        )

        await connection.close()

        controllers: list[TriviaGameController] = list()

        if records is not None and len(records) >= 1:
            for record in records:
                controllers.append(TriviaGameController(
                    twitchChannel = twitchChannel,
                    twitchChannelId = record[0],
                    userId = record[1],
                    userName = record[2]
                ))

            controllers.sort(key = lambda controller: controller.userName.casefold())

        frozenControllers: FrozenList[TriviaGameController] = FrozenList(controllers)
        frozenControllers.freeze()
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
            self.__timber.log('TriviaGameControllersRepository', f'Unable to find userId when trying to remove user as a trivia game controller ({twitchChannelId=}) ({userName=}): {e}', e, traceback.format_exc())
            return RemoveTriviaGameControllerResult.ERROR

        connection = await self.__backingDatabase.getConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM triviagamecontrollers
                WHERE twitchchannelid = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannelId, userId
        )

        if record is None or len(record) < 1:
            await connection.close()
            self.__timber.log('TriviaGameControllersRepository', f'Tried to remove trivia game controller, but they\'re not already added ({twitchChannelId=}) ({userName=}) ({userId=})')
            return RemoveTriviaGameControllerResult.DOES_NOT_EXIST

        self.__cache.pop(twitchChannelId, None)

        await connection.execute(
            '''
                DELETE FROM triviagamecontrollers
                WHERE twitchchannelid = $1 AND userid = $2
            ''',
            twitchChannelId, userId
        )

        await connection.close()
        self.__timber.log('TriviaGameControllersRepository', f'Finished removing trivia game controller ({twitchChannelId=}) ({userName=}) ({userId=})')
        return RemoveTriviaGameControllerResult.REMOVED
