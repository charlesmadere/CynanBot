from .triviaScoreRepositoryInterface import TriviaScoreRepositoryInterface
from .triviaScoreResult import TriviaScoreResult
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType


class TriviaScoreRepository(TriviaScoreRepositoryInterface):

    def __init__(self, backingDatabase: BackingDatabase):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase

        self.__isDatabaseReady: bool = False

    async def fetchTriviaScore(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> TriviaScoreResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT streak, supertriviawins, trivialosses, triviawins, twitchchannelid, userid FROM triviascores
                WHERE twitchchannelid = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannelId, userId
        )

        if record is not None and len(record) >= 1:
            result = TriviaScoreResult(
                streak = record[0],
                superTriviaWins = record[1],
                triviaLosses = record[2],
                triviaWins = record[3],
                twitchChannel = record[4],
                twitchChannelId = twitchChannelId,
                userId = record[5]
            )

            await connection.close()
            return result

        await connection.execute(
            '''
                INSERT INTO triviascores (streak, supertriviawins, trivialosses, triviawins, twitchchannelid, userid)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''',
            0, 0, 0, 0, twitchChannelId, userId
        )

        await connection.close()

        return TriviaScoreResult(
            streak = 0,
            superTriviaWins = 0,
            triviaLosses = 0,
            triviaWins = 0,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def incrementSuperTriviaWins(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> TriviaScoreResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.fetchTriviaScore(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

        newSuperTriviaWins = result.getSuperTriviaWins() + 1

        newResult = TriviaScoreResult(
            streak = result.getStreak(),
            superTriviaWins = newSuperTriviaWins,
            triviaLosses = result.getTriviaLosses(),
            triviaWins = result.getTriviaWins(),
            twitchChannel = result.getTwitchChannel(),
            twitchChannelId = result.getTwitchChannelId(),
            userId = result.getUserId()
        )

        await self.__updateTriviaScore(
            newStreak = newResult.getStreak(),
            newSuperTriviaWins = newResult.getSuperTriviaWins(),
            newTriviaLosses = newResult.getTriviaLosses(),
            newTriviaWins = newResult.getTriviaWins(),
            twitchChannel = newResult.getTwitchChannel(),
            twitchChannelId = newResult.getTwitchChannelId(),
            userId = newResult.getUserId()
        )

        return newResult

    async def incrementTriviaLosses(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> TriviaScoreResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.fetchTriviaScore(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

        newStreak: int
        if result.getStreak() <= -1:
            newStreak = result.getStreak() - 1
        else:
            newStreak = -1

        newTriviaLosses: int = result.getTriviaLosses() + 1

        newResult = TriviaScoreResult(
            streak = newStreak,
            superTriviaWins = result.getSuperTriviaWins(),
            triviaLosses = newTriviaLosses,
            triviaWins = result.getTriviaWins(),
            twitchChannel = result.getTwitchChannel(),
            twitchChannelId = result.getTwitchChannelId(),
            userId = result.getUserId()
        )

        await self.__updateTriviaScore(
            newStreak = newResult.getStreak(),
            newSuperTriviaWins = newResult.getSuperTriviaWins(),
            newTriviaLosses = newResult.getTriviaLosses(),
            newTriviaWins = newResult.getTriviaWins(),
            twitchChannel = newResult.getTwitchChannel(),
            twitchChannelId = newResult.getTwitchChannelId(),
            userId = newResult.getUserId()
        )

        return newResult

    async def incrementTriviaWins(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> TriviaScoreResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.fetchTriviaScore(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

        newStreak: int
        if result.getStreak() >= 1:
            newStreak = result.getStreak() + 1
        else:
            newStreak = 1

        newTriviaWins = result.getTriviaWins() + 1

        newResult = TriviaScoreResult(
            streak = newStreak,
            superTriviaWins = result.getSuperTriviaWins(),
            triviaLosses = result.getTriviaLosses(),
            triviaWins = newTriviaWins,
            twitchChannel = result.getTwitchChannel(),
            twitchChannelId = result.getTwitchChannelId(),
            userId = result.getUserId()
        )

        await self.__updateTriviaScore(
            newStreak = newResult.getStreak(),
            newSuperTriviaWins = newResult.getSuperTriviaWins(),
            newTriviaLosses = newResult.getTriviaLosses(),
            newTriviaWins = newResult.getTriviaWins(),
            twitchChannel = newResult.getTwitchChannel(),
            twitchChannelId = newResult.getTwitchChannelId(),
            userId = newResult.getUserId()
        )

        return newResult

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS triviascores (
                            streak integer DEFAULT 0 NOT NULL,
                            supertriviawins integer DEFAULT 0 NOT NULL,
                            trivialosses integer DEFAULT 0 NOT NULL,
                            triviawins integer DEFAULT 0 NOT NULL,
                            twitchchannelid text NOT NULL,
                            userid text NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS triviascores (
                            streak INTEGER NOT NULL DEFAULT 0,
                            supertriviawins INTEGER NOT NULL DEFAULT 0,
                            trivialosses INTEGER NOT NULL DEFAULT 0,
                            triviawins INTEGER NOT NULL DEFAULT 0,
                            twitchchannelid TEXT NOT NULL,
                            userid TEXT NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def __updateTriviaScore(
        self,
        newStreak: int,
        newSuperTriviaWins: int,
        newTriviaLosses: int,
        newTriviaWins: int,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ):
        if not utils.isValidInt(newStreak):
            raise TypeError(f'newStreak argument is malformed: \"{newStreak}\"')
        elif newStreak < utils.getIntMinSafeSize() or newStreak > utils.getIntMaxSafeSize():
            raise ValueError(f'newStreak argument is out of boudns: {newStreak}')
        elif not utils.isValidInt(newSuperTriviaWins):
            raise TypeError(f'newSuperTriviaWins argument is malformed: \"{newSuperTriviaWins}\"')
        elif newSuperTriviaWins < 0 or newSuperTriviaWins > utils.getIntMaxSafeSize():
            raise ValueError(f'newSuperTriviaWins argument is out of bounds: {newSuperTriviaWins}')
        elif not utils.isValidInt(newTriviaLosses):
            raise TypeError(f'newTriviaLosses argument is malformed: \"{newTriviaLosses}\"')
        elif newTriviaLosses < 0 or newTriviaLosses > utils.getIntMaxSafeSize():
            raise ValueError(f'newTriviaLosses argument is out of bounds: {newTriviaLosses}')
        elif not utils.isValidInt(newTriviaWins):
            raise TypeError(f'newTriviaWins argument is malformed: \"{newTriviaWins}\"')
        elif newTriviaWins < 0 or newTriviaLosses > utils.getIntMaxSafeSize():
            raise ValueError(f'newTriviaWins argument is out of bounds: {newTriviaWins}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__backingDatabase.getConnection()
        await connection.execute(
            '''
                INSERT INTO triviascores (streak, supertriviawins, trivialosses, triviawins, twitchchannelid, userid)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (twitchchannelid, userid) DO UPDATE SET streak = EXCLUDED.streak, supertriviawins = EXCLUDED.supertriviawins, triviaLosses = EXCLUDED.trivialosses, triviawins = EXCLUDED.triviawins
            ''',
            newStreak, newSuperTriviaWins, newTriviaLosses, newTriviaWins, twitchChannelId, userId
        )

        await connection.close()
