import CynanBot.misc.utils as utils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.trivia.score.triviaScoreRepositoryInterface import \
    TriviaScoreRepositoryInterface
from CynanBot.trivia.score.triviaScoreResult import TriviaScoreResult


class TriviaScoreRepository(TriviaScoreRepositoryInterface):

    def __init__(self, backingDatabase: BackingDatabase):
        assert isinstance(backingDatabase, BackingDatabase), f"malformed {backingDatabase=}"

        self.__backingDatabase: BackingDatabase = backingDatabase

        self.__isDatabaseReady: bool = False

    async def fetchTriviaScore(
        self,
        twitchChannel: str,
        userId: str
    ) -> TriviaScoreResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT streak, supertriviawins, trivialosses, triviawins, twitchchannel, userid FROM triviascores
                WHERE twitchchannel = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannel, userId
        )

        if utils.hasItems(record):
            result = TriviaScoreResult(
                streak = record[0],
                superTriviaWins = record[1],
                triviaLosses = record[2],
                triviaWins = record[3],
                twitchChannel = record[4],
                userId = record[5]
            )

            await connection.close()
            return result

        await connection.execute(
            '''
                INSERT INTO triviascores (streak, supertriviawins, trivialosses, triviawins, twitchchannel, userid)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''',
            0, 0, 0, 0, twitchChannel, userId
        )

        await connection.close()
        return TriviaScoreResult(
            streak = 0,
            superTriviaWins = 0,
            triviaLosses = 0,
            triviaWins = 0,
            twitchChannel = twitchChannel,
            userId = userId
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def incrementSuperTriviaWins(
        self,
        twitchChannel: str,
        userId: str
    ) -> TriviaScoreResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        result = await self.fetchTriviaScore(
            twitchChannel = twitchChannel,
            userId = userId
        )

        newSuperTriviaWins: int = result.getSuperTriviaWins() + 1

        newResult = TriviaScoreResult(
            streak = result.getStreak(),
            superTriviaWins = newSuperTriviaWins,
            triviaLosses = result.getTriviaLosses(),
            triviaWins = result.getTriviaWins(),
            twitchChannel = result.getTwitchChannel(),
            userId = result.getUserId()
        )

        await self.__updateTriviaScore(
            newStreak = newResult.getStreak(),
            newSuperTriviaWins = newResult.getSuperTriviaWins(),
            newTriviaLosses = newResult.getTriviaLosses(),
            newTriviaWins = newResult.getTriviaWins(),
            twitchChannel = newResult.getTwitchChannel(),
            userId = newResult.getUserId()
        )

        return newResult

    async def incrementTriviaLosses(
        self,
        twitchChannel: str,
        userId: str
    ) -> TriviaScoreResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        result = await self.fetchTriviaScore(
            twitchChannel = twitchChannel,
            userId = userId
        )

        newStreak: int = 0
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
            userId = result.getUserId()
        )

        await self.__updateTriviaScore(
            newStreak = newResult.getStreak(),
            newSuperTriviaWins = newResult.getSuperTriviaWins(),
            newTriviaLosses = newResult.getTriviaLosses(),
            newTriviaWins = newResult.getTriviaWins(),
            twitchChannel = newResult.getTwitchChannel(),
            userId = newResult.getUserId()
        )

        return newResult

    async def incrementTriviaWins(
        self,
        twitchChannel: str,
        userId: str
    ) -> TriviaScoreResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        result = await self.fetchTriviaScore(
            twitchChannel = twitchChannel,
            userId = userId
        )

        newStreak: int = 0
        if result.getStreak() >= 1:
            newStreak = result.getStreak() + 1
        else:
            newStreak = 1

        newTriviaWins: int = result.getTriviaWins() + 1

        newResult = TriviaScoreResult(
            streak = newStreak,
            superTriviaWins = result.getSuperTriviaWins(),
            triviaLosses = result.getTriviaLosses(),
            triviaWins = newTriviaWins,
            twitchChannel = result.getTwitchChannel(),
            userId = result.getUserId()
        )

        await self.__updateTriviaScore(
            newStreak = newResult.getStreak(),
            newSuperTriviaWins = newResult.getSuperTriviaWins(),
            newTriviaLosses = newResult.getTriviaLosses(),
            newTriviaWins = newResult.getTriviaWins(),
            twitchChannel = newResult.getTwitchChannel(),
            userId = newResult.getUserId()
        )

        return newResult

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviascores (
                        streak integer DEFAULT 0 NOT NULL,
                        supertriviawins integer DEFAULT 0 NOT NULL,
                        trivialosses integer DEFAULT 0 NOT NULL,
                        triviawins integer DEFAULT 0 NOT NULL,
                        twitchchannel public.citext NOT NULL,
                        userid public.citext NOT NULL,
                        PRIMARY KEY (twitchchannel, userid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviascores (
                        streak INTEGER NOT NULL DEFAULT 0,
                        supertriviawins INTEGER NOT NULL DEFAULT 0,
                        trivialosses INTEGER NOT NULL DEFAULT 0,
                        triviawins INTEGER NOT NULL DEFAULT 0,
                        twitchchannel TEXT NOT NULL COLLATE NOCASE,
                        userid TEXT NOT NULL COLLATE NOCASE,
                        PRIMARY KEY (twitchchannel, userid)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def __updateTriviaScore(
        self,
        newStreak: int,
        newSuperTriviaWins: int,
        newTriviaLosses: int,
        newTriviaWins: int,
        twitchChannel: str,
        userId: str
    ):
        if not utils.isValidInt(newStreak):
            raise ValueError(f'newStreak argument is malformed: \"{newStreak}\"')
        if newStreak < utils.getIntMinSafeSize() or newStreak > utils.getIntMaxSafeSize():
            raise ValueError(f'newStreak argument is out of boudns: {newStreak}')
        if not utils.isValidInt(newSuperTriviaWins):
            raise ValueError(f'newSuperTriviaWins argument is malformed: \"{newSuperTriviaWins}\"')
        if newSuperTriviaWins < 0 or newSuperTriviaWins > utils.getIntMaxSafeSize():
            raise ValueError(f'newSuperTriviaWins argument is out of bounds: {newSuperTriviaWins}')
        if not utils.isValidInt(newTriviaLosses):
            raise ValueError(f'newTriviaLosses argument is malformed: \"{newTriviaLosses}\"')
        if newTriviaLosses < 0 or newTriviaLosses > utils.getIntMaxSafeSize():
            raise ValueError(f'newTriviaLosses argument is out of bounds: {newTriviaLosses}')
        if not utils.isValidInt(newTriviaWins):
            raise ValueError(f'newTriviaWins argument is malformed: \"{newTriviaWins}\"')
        if newTriviaWins < 0 or newTriviaLosses > utils.getIntMaxSafeSize():
            raise ValueError(f'newTriviaWins argument is out of bounds: {newTriviaWins}')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__backingDatabase.getConnection()
        await connection.execute(
            '''
                INSERT INTO triviascores (streak, supertriviawins, trivialosses, triviawins, twitchchannel, userid)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (twitchchannel, userid) DO UPDATE SET streak = EXCLUDED.streak, supertriviawins = EXCLUDED.supertriviawins, triviaLosses = EXCLUDED.trivialosses, triviawins = EXCLUDED.triviawins
            ''',
            newStreak, newSuperTriviaWins, newTriviaLosses, newTriviaWins, twitchChannel, userId
        )

        await connection.close()
