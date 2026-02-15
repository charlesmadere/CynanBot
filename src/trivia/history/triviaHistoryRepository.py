from datetime import datetime, timedelta
from typing import Final

from .triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from ..content.triviaContentCode import TriviaContentCode
from ..misc.triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from ..misc.triviaSourceParserInterface import TriviaSourceParserInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaQuestionReference import TriviaQuestionReference
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class TriviaHistoryRepository(TriviaHistoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        triviaQuestionTypeParser: TriviaQuestionTypeParserInterface,
        triviaSettings: TriviaSettingsInterface,
        triviaSourceParser: TriviaSourceParserInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(triviaQuestionTypeParser, TriviaQuestionTypeParserInterface):
            raise TypeError(f'triviaQuestionTypeParser argument is malformed: \"{triviaQuestionTypeParser}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')
        elif not isinstance(triviaSourceParser, TriviaSourceParserInterface):
            raise TypeError(f'triviaSourceParser argument is malformed: \"{triviaSourceParser}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__triviaQuestionTypeParser: Final[TriviaQuestionTypeParserInterface] = triviaQuestionTypeParser
        self.__triviaSettings: Final[TriviaSettingsInterface] = triviaSettings
        self.__triviaSourceParser: Final[TriviaSourceParserInterface] = triviaSourceParser

        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getMostRecentTriviaQuestionDetails(
        self,
        emote: str,
        twitchChannel: str,
        twitchChannelId: str,
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
                SELECT datetime, emote, triviaid, triviasource, triviatype FROM triviahistory
                WHERE emote IS NOT NULL AND emote = $1 AND twitchchannelid = $2
                ORDER BY datetime DESC
                LIMIT 1
            ''',
            emote, twitchChannelId,
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        return TriviaQuestionReference(
            dateTime = datetime.fromisoformat(record[0]),
            emote = record[1],
            triviaId = record[2],
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            triviaSource = await self.__triviaSourceParser.parse(record[3]),
            triviaType = await self.__triviaQuestionTypeParser.parse(record[4]),
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

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS triviahistory (
                            datetime TEXT NOT NULL,
                            emote TEXT NOT NULL,
                            triviaid TEXT NOT NULL,
                            triviasource TEXT NOT NULL,
                            triviatype TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (triviaid, triviasource, triviatype, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def verify(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        twitchChannel: str,
        twitchChannelId: str,
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

        triviaSource = await self.__triviaSourceParser.serialize(workingTriviaSource)
        triviaType = await self.__triviaQuestionTypeParser.serialize(question.triviaType)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT datetime FROM triviahistory
                WHERE triviaid = $1 AND triviasource = $2 AND triviatype = $3 AND twitchchannelid = $4
                LIMIT 1
            ''',
            question.triviaId, triviaSource, triviaType, twitchChannelId,
        )

        nowDateTime = datetime.now(self.__timeZoneRepository.getDefault())
        nowDateTimeStr = nowDateTime.isoformat()

        if record is None or len(record) == 0:
            await connection.execute(
                '''
                    INSERT INTO triviahistory (datetime, emote, triviaid, triviasource, triviatype, twitchchannelid)
                    VALUES ($1, $2, $3, $4, $5, $6)
                ''',
                nowDateTimeStr, emote, question.triviaId, triviaSource, triviaType, twitchChannelId,
            )

            await connection.close()
            return TriviaContentCode.OK

        questionDateTimeStr: str = record[0]
        questionDateTime = datetime.fromisoformat(questionDateTimeStr)
        minimumTimeDelta = timedelta(days = await self.__triviaSettings.getMinDaysBeforeRepeatQuestion())

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
            nowDateTimeStr, emote, question.triviaId, triviaSource, triviaType, twitchChannelId,
        )

        await connection.close()
        self.__timber.log('TriviaHistoryRepository', f'Updated triviaHistory entry ({nowDateTimeStr=}) ({questionDateTimeStr=}) ({emote=}) ({workingTriviaSource=}) ({question.originalTriviaSource=}) ({question.triviaId=}) ({question.triviaSource=}) ({question.triviaType=}) ({twitchChannel=}) ({twitchChannelId=})')
        return TriviaContentCode.OK
