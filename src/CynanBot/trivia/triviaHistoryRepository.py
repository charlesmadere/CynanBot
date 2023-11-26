from datetime import datetime, timedelta, timezone
from typing import Optional

import misc.utils as utils
from storage.backingDatabase import BackingDatabase
from storage.databaseConnection import DatabaseConnection
from storage.databaseType import DatabaseType
from timber.timberInterface import TimberInterface
from trivia.absTriviaQuestion import AbsTriviaQuestion
from trivia.triviaContentCode import TriviaContentCode
from trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from trivia.triviaQuestionReference import TriviaQuestionReference
from trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from trivia.triviaSource import TriviaSource
from trivia.triviaType import TriviaType


class TriviaHistoryRepository(TriviaHistoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise ValueError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__timeZone: timezone = timeZone

        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getMostRecentTriviaQuestionDetails(
        self,
        emote: str,
        twitchChannel: str
    ) -> Optional[TriviaQuestionReference]:
        if not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT emote, triviaid, triviasource, triviatype FROM triviahistory
                WHERE emote IS NOT NULL AND emote = $1 AND twitchchannel = $2
                ORDER BY datetime DESC
                LIMIT 1
            ''',
            emote, twitchChannel
        )

        await connection.close()

        if not utils.hasItems(record):
            return None

        return TriviaQuestionReference(
            emote = record[0],
            triviaId = record[1],
            twitchChannel = twitchChannel,
            triviaSource = TriviaSource.fromStr(record[2]),
            triviaType = TriviaType.fromStr(record[3])
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
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

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

        if not utils.hasItems(record):
            await connection.execute(
                '''
                    INSERT INTO triviahistory (datetime, emote, triviaid, triviasource, triviatype, twitchchannel)
                    VALUES ($1, $2, $3, $4, $5, $6)
                ''',
                nowDateTimeStr, emote, triviaId, triviaSource, triviaType, twitchChannel
            )

            await connection.close()
            return TriviaContentCode.OK

        questionDateTimeStr: str = record[0]
        questionDateTime = datetime.fromisoformat(questionDateTimeStr)
        minimumTimeDelta = timedelta(days = await self.__triviaSettingsRepository.getMinDaysBeforeRepeatQuestion())

        if questionDateTime + minimumTimeDelta >= nowDateTime:
            await connection.close()
            self.__timber.log('TriviaHistoryRepository', f'Encountered duplicate triviaHistory entry that is within the window of being a repeat (now=\"{nowDateTimeStr}\" db=\"{questionDateTimeStr}\" triviaId=\"{triviaId}\" triviaSource=\"{triviaSource}\" twitchChannel=\"{twitchChannel}\"')
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
        self.__timber.log('TriviaHistoryRepository', f'Updated triviaHistory entry to {nowDateTimeStr} from {questionDateTimeStr} (triviaId=\"{triviaId}\" triviaSource=\"{triviaSource}\" triviaType=\"{triviaType}\" twitchChannel=\"{twitchChannel}\")')

        return TriviaContentCode.OK
