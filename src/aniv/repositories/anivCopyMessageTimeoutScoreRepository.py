from datetime import datetime
from typing import Final

from .anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from ..models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType


class AnivCopyMessageTimeoutScoreRepository(AnivCopyMessageTimeoutScoreRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getScore(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AnivCopyMessageTimeoutScore:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT mostrecentdodge, mostrecenttimeout, dodgescore, timeoutscore FROM anivcopymessagetimeoutscores
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()

        if record is None or len(record) == 0:
            return AnivCopyMessageTimeoutScore(
                mostRecentDodge = None,
                mostRecentTimeout = None,
                dodgeScore = 0,
                timeoutScore = 0,
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        mostRecentDodge: datetime | None = None
        if utils.isValidStr(record[0]):
            mostRecentDodge = datetime.fromisoformat(record[0])

        mostRecentTimeout: datetime | None = None
        if utils.isValidStr(record[1]):
            mostRecentTimeout = datetime.fromisoformat(record[1])

        return AnivCopyMessageTimeoutScore(
            mostRecentDodge = mostRecentDodge,
            mostRecentTimeout = mostRecentTimeout,
            dodgeScore = record[2],
            timeoutScore = record[3],
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

    async def incrementDodgeScore(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AnivCopyMessageTimeoutScore:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        score = await self.getScore(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        score = AnivCopyMessageTimeoutScore(
            mostRecentDodge = datetime.now(self.__timeZoneRepository.getDefault()),
            mostRecentTimeout = score.mostRecentTimeout,
            dodgeScore = score.dodgeScore + 1,
            timeoutScore = score.timeoutScore,
            chatterUserId = score.chatterUserId,
            twitchChannelId = score.twitchChannelId,
        )

        await self.__saveScoreToDatabase(score)
        return score

    async def incrementTimeoutScore(
        self,
        timeoutDurationSeconds: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AnivCopyMessageTimeoutScore:
        if not utils.isValidInt(timeoutDurationSeconds):
            raise TypeError(f'timeoutDurationSeconds argument is malformed: \"{timeoutDurationSeconds}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        score = await self.getScore(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        score = AnivCopyMessageTimeoutScore(
            mostRecentDodge = score.mostRecentDodge,
            mostRecentTimeout = datetime.now(self.__timeZoneRepository.getDefault()),
            dodgeScore = score.dodgeScore,
            timeoutScore = score.timeoutScore + 1,
            chatterUserId = score.chatterUserId,
            twitchChannelId = score.twitchChannelId,
        )

        await self.__saveScoreToDatabase(score)
        return score

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS anivcopymessagetimeoutscores (
                            mostrecentdodge text DEFAULT NULL,
                            mostrecenttimeout text DEFAULT NULL,
                            dodgescore int DEFAULT 0 NOT NULL,
                            timeoutscore int DEFAULT 0 NOT NULL,
                            chatteruserid text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS anivcopymessagetimeoutscores (
                            mostrecentdodge TEXT DEFAULT NULL,
                            mostrecenttimeout TEXT DEFAULT NULL,
                            dodgescore INTEGER NOT NULL DEFAULT 0,
                            timeoutscore INTEGER NOT NULL DEFAULT 0,
                            chatteruserid TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

    async def __saveScoreToDatabase(self, score: AnivCopyMessageTimeoutScore):
        if not isinstance(score, AnivCopyMessageTimeoutScore):
            raise TypeError(f'score argument is malformed: \"{score}\"')

        mostRecentDodge: str | None = None
        if isinstance(score.mostRecentDodge, datetime):
            mostRecentDodge = score.mostRecentDodge.isoformat()

        mostRecentTimeout: str | None = None
        if isinstance(score.mostRecentTimeout, datetime):
            mostRecentTimeout = score.mostRecentTimeout.isoformat()

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO anivcopymessagetimeoutscores (mostrecentdodge, mostrecenttimeout, dodgescore, timeoutscore, chatteruserid, twitchchannelid)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET mostrecentdodge = EXCLUDED.mostrecentdodge, mostrecenttimeout = EXCLUDED.mostrecenttimeout, dodgescore = EXCLUDED.dodgescore, timeoutscore = EXCLUDED.timeoutscore
            ''',
            mostRecentDodge, mostRecentTimeout, score.dodgeScore, score.timeoutScore, score.chatterUserId, score.twitchChannelId
        )

        await connection.close()
