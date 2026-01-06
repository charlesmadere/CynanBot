from typing import Final

from .banTriviaQuestionResult import BanTriviaQuestionResult
from .bannedTriviaIdsRepositoryInterface import \
    BannedTriviaIdsRepositoryInterface
from .bannedTriviaQuestion import BannedTriviaQuestion
from ..misc.triviaSourceParserInterface import TriviaSourceParserInterface
from ..questions.triviaSource import TriviaSource
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class BannedTriviaIdsRepository(BannedTriviaIdsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        triviaSourceParser: TriviaSourceParserInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSourceParser, TriviaSourceParserInterface):
            raise TypeError(f'triviaSourceParser argument is malformed: \"{triviaSourceParser}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__triviaSourceParser: Final[TriviaSourceParserInterface] = triviaSourceParser

        self.__isDatabaseReady: bool = False

    async def ban(
        self,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource,
    ) -> BanTriviaQuestionResult:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        info = await self.getInfo(
            triviaId = triviaId,
            triviaSource = triviaSource,
        )

        if info is not None:
            self.__timber.log('BannedTriviaIdsRepository', f'Attempted to ban trivia question but it\'s already been banned: {info}')
            return BanTriviaQuestionResult.ALREADY_BANNED

        self.__timber.log('BannedTriviaIdsRepository', f'Banning trivia question (triviaId=\"{triviaId}\", userId=\"{userId}\", triviaSource=\"{triviaSource}\")...')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO bannedtriviaids (triviaid, triviasource, userid)
                VALUES ($1, $2, $3)
            ''',
            triviaId, triviaSource.toStr(), userId
        )

        await connection.close()
        self.__timber.log('BannedTriviaIdsRepository', f'Banned trivia question (triviaId=\"{triviaId}\", userId=\"{userId}\", triviaSource=\"{triviaSource}\")')

        return BanTriviaQuestionResult.BANNED

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getInfo(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
    ) -> BannedTriviaQuestion | None:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT bannedtriviaids.triviaid, bannedtriviaids.triviasource, bannedtriviaids.userid, userids.username FROM bannedtriviaids
                INNER JOIN userids ON bannedtriviaids.userid = userids.userid
                WHERE bannedtriviaids.triviaid = $1 AND bannedtriviaids.triviasource = $2
                LIMIT 1
            ''',
            triviaId, triviaSource.toStr()
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        return BannedTriviaQuestion(
            triviaId = record[0],
            userId = record[2],
            userName = record[3],
            triviaSource = await self.__triviaSourceParser.parse(record[1]),
        )

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS bannedtriviaids (
                            triviaid public.citext NOT NULL,
                            triviasource public.citext NOT NULL,
                            userid text NOT NULL,
                            PRIMARY KEY (triviaid, triviasource)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS bannedtriviaids (
                            triviaid TEXT NOT NULL COLLATE NOCASE,
                            triviasource TEXT NOT NULL COLLATE NOCASE,
                            userid TEXT NOT NULL,
                            PRIMARY KEY (triviaid, triviasource)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def isBanned(self, triviaId: str, triviaSource: TriviaSource) -> bool:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        info = await self.getInfo(
            triviaId = triviaId,
            triviaSource = triviaSource,
        )

        if info is None:
            return False

        self.__timber.log('BannedTriviaIdsRepository', f'Encountered banned trivia question ({info})')
        return True

    async def unban(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> BanTriviaQuestionResult:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        info = await self.getInfo(
            triviaId = triviaId,
            triviaSource = triviaSource,
        )

        if info is None:
            self.__timber.log('BannedTriviaIdsRepository', f'Attempted to unban trivia question but it wasn\'t banned (triviaId=\"{triviaId}\", triviaSource=\"{triviaSource}\")')
            return BanTriviaQuestionResult.NOT_BANNED

        self.__timber.log('BannedTriviaIdsRepository', f'Unbanning trivia question (triviaId=\"{triviaId}\", triviaSource=\"{triviaSource}\")...')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM bannedtriviaids
                WHERE triviaid = $1 AND triviasource = $2
            ''',
            triviaId, triviaSource.toStr()
        )

        await connection.close()
        self.__timber.log('BannedTriviaIdsRepository', f'Unbanned trivia question (triviaId=\"{triviaId}\", triviaSource=\"{triviaSource}\")')
        return BanTriviaQuestionResult.UNBANNED
