from .triviaQuestionOccurrences import TriviaQuestionOccurrences
from .triviaQuestionOccurrencesRepositoryInterface import TriviaQuestionOccurrencesRepositoryInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaSource import TriviaSource
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class TriviaQuestionOccurrencesRepository(TriviaQuestionOccurrencesRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getOccurrences(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> TriviaQuestionOccurrences:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        connection = await self.__getDatabaseConnection()
        occurrences = await self.__getOccurrences(
            connection = connection,
            triviaId = triviaId,
            triviaSource = triviaSource
        )

        await connection.close()
        return occurrences

    async def __getOccurrences(
        self,
        connection: DatabaseConnection,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> TriviaQuestionOccurrences:
        record = await connection.fetchRow(
            '''
                SELECT occurrences FROM triviaquestionoccurrences
                WHERE triviaid = $1 AND triviasource = $2
                LIMIT 1
            ''',
            triviaId, triviaSource.toStr()
        )

        if record is None or len(record) == 0:
            return TriviaQuestionOccurrences(
                occurrences = 0,
                triviaId = triviaId,
                triviaSource = triviaSource
            )
        else:
            return TriviaQuestionOccurrences(
                occurrences = record[0],
                triviaId = triviaId,
                triviaSource = triviaSource
            )

    async def getOccurrencesFromQuestion(
        self,
        triviaQuestion: AbsTriviaQuestion
    ) -> TriviaQuestionOccurrences:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')

        workingTriviaSource = triviaQuestion.triviaSource
        if triviaQuestion.originalTriviaSource is not None:
            workingTriviaSource = triviaQuestion.originalTriviaSource

        return await self.getOccurrences(
            triviaId = triviaQuestion.triviaId,
            triviaSource = workingTriviaSource
        )

    async def incrementOccurrences(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> TriviaQuestionOccurrences:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        connection = await self.__getDatabaseConnection()

        occurrences = await self.__getOccurrences(
            connection = connection,
            triviaId = triviaId,
            triviaSource = triviaSource
        )

        newOccurrences = TriviaQuestionOccurrences(
            occurrences = occurrences.occurrences + 1,
            triviaId = triviaId,
            triviaSource = triviaSource
        )

        await connection.execute(
            '''
                INSERT INTO triviaquestionoccurrences
                VALUES ($1, $2, $3)
                ON CONFLICT (triviaid, triviasource) DO UPDATE SET occurrences = EXCLUDED.occurrences
            ''',
            newOccurrences.occurrences, triviaId, triviaSource.toStr()
        )

        await connection.close()
        return newOccurrences

    async def incrementOccurrencesFromQuestion(
        self,
        triviaQuestion: AbsTriviaQuestion
    ) -> TriviaQuestionOccurrences:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')

        workingTriviaSource = triviaQuestion.triviaSource
        if triviaQuestion.originalTriviaSource is not None:
            workingTriviaSource = triviaQuestion.originalTriviaSource

        return await self.incrementOccurrences(
            triviaId = triviaQuestion.triviaId,
            triviaSource = workingTriviaSource
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
                        CREATE TABLE IF NOT EXISTS triviaquestionoccurrences (
                            occurrences int DEFAULT 0 NOT NULL,
                            triviaid text NOT NULL,
                            triviasource text NOT NULL,
                            PRIMARY KEY (triviaid, triviasource)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS triviaquestionoccurrences (
                            occurrences INTEGER NOT NULL DEFAULT 0,
                            triviaid TEXT NOT NULL,
                            triviasource TEXT NOT NULL,
                            PRIMARY KEY (triviaid, triviasource)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
