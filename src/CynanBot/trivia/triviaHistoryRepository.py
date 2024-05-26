from datetime import datetime, timedelta

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
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
        timeZoneRepository: TimeZoneRepositoryInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getMostRecentTriviaQuestionDetails(
        self,
        emote: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TriviaQuestionReference | None:
        if not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT emote, triviaid, triviasource, triviatype FROM triviahistory
                WHERE emote IS NOT NULL AND emote = $1 AND twitchchannelid = $2
                ORDER BY datetime DESC
                LIMIT 1
            ''',
            emote, twitchChannelId
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        return TriviaQuestionReference(
            emote = record[0],
            triviaId = record[1],
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            triviaSource = TriviaSource.fromStr(record[2]),
            triviaType = TriviaQuestionType.fromStr(record[3])
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
                        triviaid text NOT NULL,
                        triviasource text NOT NULL,
                        triviatype text NOT NULL,
                        twitchchannelid text NOT NULL,
                        PRIMARY KEY (triviaid, triviasource, triviatype, twitchchannelid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviahistory (
                        datetime TEXT NOT NULL,
                        emote TEXT NOT NULL,
                        triviaid TEXT NOT NULL,
                        triviasource TEXT NOT NULL,
                        triviatype TEXT NOT NULL,
                        twitchchannelid TEXT NOT NULL,
                        PRIMARY KEY (triviaid, triviasource, triviatype, twitchchannelid)
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
        twitchChannel: str,
        twitchChannelId: str
    ) -> TriviaContentCode:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        workingTriviaSource = question.triviaSource
        if question.originalTriviaSource is not None:
            workingTriviaSource = question.originalTriviaSource

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT datetime FROM triviahistory
                WHERE triviaid = $1 AND triviasource = $2 AND triviatype = $3 AND twitchchannelid = $4
                LIMIT 1
            ''',
            question.triviaId, workingTriviaSource.toStr(), question.triviaType.toStr(), twitchChannelId
        )

        nowDateTime = datetime.now(self.__timeZoneRepository.getDefault())
        nowDateTimeStr = nowDateTime.isoformat()

        if record is None or len(record) == 0:
            await connection.execute(
                '''
                    INSERT INTO triviahistory (datetime, emote, triviaid, triviasource, triviatype, twitchchannelid)
                    VALUES ($1, $2, $3, $4, $5, $6)
                ''',
                nowDateTimeStr, emote, question.triviaId, workingTriviaSource.toStr(), question.triviaType.toStr(), twitchChannelId
            )

            await connection.close()
            return TriviaContentCode.OK

        questionDateTimeStr: str = record[0]
        questionDateTime = datetime.fromisoformat(questionDateTimeStr)
        minimumTimeDelta = timedelta(days = await self.__triviaSettingsRepository.getMinDaysBeforeRepeatQuestion())

        if questionDateTime + minimumTimeDelta >= nowDateTime:
            await connection.close()
            self.__timber.log('TriviaHistoryRepository', f'Encountered duplicate triviaHistory entry that is within the window of being a repeat ({nowDateTimeStr=}) ({questionDateTimeStr=}) ({emote=}) ({workingTriviaSource=}) ({question.originalTriviaSource=}) ({question.triviaId=}) ({question.triviaSource=}) ({question.triviaType=}) ({twitchChannel=}) ({twitchChannelId=})')
            return TriviaContentCode.REPEAT

        await connection.execute(
            '''
                UPDATE triviahistory
                SET datetime = $1, emote = $2
                WHERE triviaid = $3 AND triviasource = $4 AND triviatype = $5 AND twitchchannelid = $6
            ''',
            nowDateTimeStr, emote, question.triviaId, question.triviaSource.toStr(), question.triviaType.toStr(), twitchChannelId
        )

        await connection.close()
        self.__timber.log('TriviaHistoryRepository', f'Updated triviaHistory entry ({nowDateTimeStr=}) ({questionDateTimeStr=}) ({emote=}) ({workingTriviaSource=}) ({question.originalTriviaSource=}) ({question.triviaId=}) ({question.triviaSource=}) ({question.triviaType=}) ({twitchChannel=}) ({twitchChannelId=})')
        return TriviaContentCode.OK
