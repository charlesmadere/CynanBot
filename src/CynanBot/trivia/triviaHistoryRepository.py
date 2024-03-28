from datetime import datetime, timedelta, timezone, tzinfo

import CynanBot.misc.utils as utils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.content.triviaContentCode import TriviaContentCode
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionReference import \
    TriviaQuestionReference
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaHistoryRepository(TriviaHistoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__timeZone: tzinfo = timeZone

        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getMostRecentTriviaQuestionDetails(
        self,
        emote: str,
        twitchChannel: str
    ) -> TriviaQuestionReference | None:
        if not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT emote, originaltriviasource, triviaid, triviasource, triviatype FROM triviahistory
                WHERE emote IS NOT NULL AND emote = $1 AND twitchchannel = $2
                ORDER BY datetime DESC
                LIMIT 1
            ''',
            emote, twitchChannel
        )

        await connection.close()

        if not utils.hasItems(record):
            return None

        originalTriviaSourceStr = record[1]
        originalTriviaSource: TriviaSource | None = None

        if utils.isValidStr(originalTriviaSourceStr):
            originalTriviaSource = TriviaSource.fromStr(originalTriviaSourceStr)

        return TriviaQuestionReference(
            emote = record[0],
            triviaId = record[2],
            twitchChannel = twitchChannel,
            originalTriviaSource = originalTriviaSource,
            triviaSource = TriviaSource.fromStr(record[3]),
            triviaType = TriviaQuestionType.fromStr(record[4])
        )

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviahistory (
                        datetime text NOT NULL,
                        emote text NOT NULL,
                        originaltriviasource public.citext DEFAULT NULL,
                        triviaid public.citext NOT NULL,
                        triviasource public.citext NOT NULL,
                        triviatype public.citext NOT NULL,
                        twitchchannel public.citext NOT NULL,
                        PRIMARY KEY (triviaid, triviasource, triviatype, twitchchannel)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviahistory (
                        datetime TEXT NOT NULL,
                        emote TEXT NOT NULL,
                        originaltriviasource TEXT DEFAULT NULL COLLATE NOCASE,
                        triviaid TEXT NOT NULL COLLATE NOCASE,
                        triviasource TEXT NOT NULL COLLATE NOCASE,
                        triviatype TEXT NOT NULL COLLATE NOCASE,
                        twitchchannel TEXT NOT NULL COLLATE NOCASE,
                        PRIMARY KEY (triviaid, triviasource, triviatype, twitchchannel)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def verify(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        twitchChannel: str
    ) -> TriviaContentCode:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        triviaId = question.getTriviaId()
        triviaSource = question.getTriviaSource().toStr()
        triviaType = question.getTriviaType().toStr()

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT datetime FROM triviahistory
                WHERE triviaid = $1 AND triviasource = $2 AND triviatype = $3 AND twitchchannel = $4
                LIMIT 1
            ''',
            triviaId, triviaSource, triviaType, twitchChannel
        )

        nowDateTime = datetime.now(self.__timeZone)
        nowDateTimeStr = nowDateTime.isoformat()

        originalTriviaSource = question.getOriginalTriviaSource()
        originalTriviaSourceStr: str | None = None

        if originalTriviaSource is not None:
            originalTriviaSourceStr = originalTriviaSource.toStr()

        if not utils.hasItems(record):
            await connection.execute(
                '''
                    INSERT INTO triviahistory (datetime, emote, originaltriviasource, triviaid, triviasource, triviatype, twitchchannel)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                ''',
                nowDateTimeStr, emote, originalTriviaSourceStr, triviaId, triviaSource, triviaType, twitchChannel
            )

            await connection.close()
            return TriviaContentCode.OK

        questionDateTimeStr: str = record[0]
        questionDateTime = datetime.fromisoformat(questionDateTimeStr)
        minimumTimeDelta = timedelta(days = await self.__triviaSettingsRepository.getMinDaysBeforeRepeatQuestion())

        if questionDateTime + minimumTimeDelta >= nowDateTime:
            await connection.close()
            self.__timber.log('TriviaHistoryRepository', f'Encountered duplicate triviaHistory entry that is within the window of being a repeat ({nowDateTimeStr=}) ({questionDateTimeStr=}) ({emote=}) ({originalTriviaSource=}) ({triviaId=}) ({triviaSource=}) ({triviaType=}) ({twitchChannel=})')
            return TriviaContentCode.REPEAT

        await connection.execute(
            '''
                UPDATE triviahistory
                SET datetime = $1, emote = $2
                WHERE triviaid = $3 AND triviasource = $4 AND triviatype = $5 AND twitchchannel = $6
            ''',
            nowDateTimeStr, emote, triviaId, triviaSource, triviaType, twitchChannel
        )

        await connection.close()
        self.__timber.log('TriviaHistoryRepository', f'Updated triviaHistory entry ({nowDateTimeStr=}) ({questionDateTimeStr=}) ({emote=}) ({originalTriviaSource=}) ({triviaId=}) ({triviaSource=}) ({triviaType=}) ({twitchChannel=})')

        return TriviaContentCode.OK
