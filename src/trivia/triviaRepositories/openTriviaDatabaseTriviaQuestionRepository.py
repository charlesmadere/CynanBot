import traceback
from typing import Any

from .absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from ..compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import (BadTriviaSessionTokenException,
                                GenericTriviaNetworkException,
                                MalformedTriviaJsonException,
                                UnsupportedTriviaTypeException)
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ..triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from ...misc import utils as utils
from ...misc.clearable import Clearable
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class OpenTriviaDatabaseTriviaQuestionRepository(AbsTriviaQuestionRepository, Clearable):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, str | None] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', 'Caches cleared')

    async def __fetchNewSessionToken(self, twitchChannelId: str) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Fetching new session token for \"{twitchChannelId}\"...')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://opentdb.com/api_token.php?command=request')
        except GenericNetworkException as e:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Encountered network error when fetching Open Trivia Database\'s session token ({twitchChannelId=}): {e}', e, traceback.format_exc())
            raise BadTriviaSessionTokenException(f'Encountered network error when fetching Open Trivia Database\'s session token ({twitchChannelId=}): {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Encountered non-200 HTTP status code ({response.getStatusCode()}) when fetching Open Trivia Database\'s session token ({twitchChannelId=})')
            raise BadTriviaSessionTokenException(f'Encountered non-200 HTTP status code ({response.getStatusCode()}) when fetching Open Trivia Database\'s session token ({twitchChannelId=})')

        jsonResponse = await response.json()
        await response.close()

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannelId \"{twitchChannelId}\" due to null/empty JSON contents: {jsonResponse}')
            raise BadTriviaSessionTokenException(f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannelId \"{twitchChannelId}\" due to null/empty JSON contents: {jsonResponse}')
        elif utils.getIntFromDict(jsonResponse, 'response_code', fallback = -1) != 0:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannelId \"{twitchChannelId}\" due to bad \"response_code\" value: {jsonResponse}')
            raise BadTriviaSessionTokenException(f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannelId \"{twitchChannelId}\" due to bad \"response_code\" value: {jsonResponse}')
        elif not utils.isValidStr(jsonResponse.get('token')):
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannelId \"{twitchChannelId}\" due to bad \"token\" value: {jsonResponse}')
            raise BadTriviaSessionTokenException(f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannelId \"{twitchChannelId}\" due to bad \"token\" value: {jsonResponse}')

        return utils.getStrFromDict(jsonResponse, 'token')

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')

        sessionToken = await self.__getOrFetchNewSessionToken(fetchOptions.twitchChannelId)
        clientSession = await self.__networkClientProvider.get()

        try:
            if utils.isValidStr(sessionToken):
                response = await clientSession.get(f'https://opentdb.com/api.php?amount=1&token={sessionToken}')
            else:
                response = await clientSession.get('https://opentdb.com/api.php?amount=1')
        except GenericNetworkException as e:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        if response.getStatusCode() != 200:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Encountered non-200 HTTP status code when fetching trivia question: \"{response.getStatusCode()}\"')
            raise GenericTriviaNetworkException(self.getTriviaSource())

        jsonResponse = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'{jsonResponse}')

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s JSON data due to null/empty JSON contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Open Trivia Database\'s JSON data due to null/empty JSON contents: {jsonResponse}')
        elif utils.getIntFromDict(jsonResponse, 'response_code', fallback = -1) != 0:
            await self.__removeSessionToken(fetchOptions.twitchChannelId)
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s JSON data due to bad \"response_code\" value: {jsonResponse}')
            raise GenericTriviaNetworkException(self.getTriviaSource())
        elif not isinstance(jsonResponse.get('results'), list):
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s JSON data due to missing/null \"results\" array: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Open Trivia Database\'s JSON data due to missing/null \"results\" array: {jsonResponse}')

        triviaJson: dict[str, Any] | None = jsonResponse['results'][0]

        if not isinstance(triviaJson, dict) or len(triviaJson) == 0:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s JSON data due to missing/null/empty \"results\" contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Open Trivia Database\'s JSON API data due to null/empty contents: {jsonResponse}')

        triviaDifficulty = TriviaDifficulty.fromStr(utils.getStrFromDict(triviaJson, 'difficulty', fallback = ''))
        triviaType = TriviaQuestionType.fromStr(utils.getStrFromDict(triviaJson, 'type'))

        category = await self.__triviaQuestionCompiler.compileQuestion(
            question = utils.getStrFromDict(triviaJson, 'category', fallback = ''),
            htmlUnescape = True
        )

        question = await self.__triviaQuestionCompiler.compileQuestion(
            question = utils.getStrFromDict(triviaJson, 'question'),
            htmlUnescape = True
        )

        triviaId = await self.__triviaIdGenerator.generateQuestionId(
            question = question,
            category = category,
            difficulty = triviaDifficulty.toStr()
        )

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = utils.getStrFromDict(triviaJson, 'correct_answer'),
                htmlUnescape = True
            )
            correctAnswerStrings: list[str] = list()
            correctAnswerStrings.append(correctAnswer)

            incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                responses = triviaJson['incorrect_answers'],
                htmlUnescape = True
            )

            multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = incorrectAnswers
            )

            if await self._verifyIsActuallyMultipleChoiceQuestion(correctAnswerStrings, multipleChoiceResponses):
                return MultipleChoiceTriviaQuestion(
                    correctAnswers = correctAnswerStrings,
                    multipleChoiceResponses = multipleChoiceResponses,
                    category = category,
                    categoryId = None,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = None,
                    triviaSource = self.getTriviaSource()
                )
            else:
                self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', 'Encountered a multiple choice question that is better suited for true/false')
                triviaType = TriviaQuestionType.TRUE_FALSE

        if triviaType is TriviaQuestionType.TRUE_FALSE:
            correctAnswer = utils.getBoolFromDict(triviaJson, 'correct_answer')

            return TrueFalseTriviaQuestion(
                correctAnswer = correctAnswer,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = None,
                triviaSource = self.getTriviaSource()
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Open Trivia Database: {jsonResponse}')

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __getOrFetchNewSessionToken(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        sessionToken = await self.__retrieveSessionToken(twitchChannelId)

        if not utils.isValidStr(sessionToken):
            try:
                sessionToken = await self.__fetchNewSessionToken(twitchChannelId)
            except BadTriviaSessionTokenException:
                pass

        await self.__storeSessionToken(
            sessionToken = sessionToken,
            twitchChannelId = twitchChannelId
        )

        return sessionToken

    def getSupportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.OPEN_TRIVIA_DATABASE

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS opentriviadatabasesessiontokens (
                        sessiontoken text DEFAULT NULL,
                        twitchchannelid text NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS opentriviadatabasesessiontokens (
                        sessiontoken TEXT DEFAULT NULL,
                        twitchchannelid TEXT NOT NULL PRIMARY KEY
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def __removeSessionToken(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        await self.__storeSessionToken(
            sessionToken = None,
            twitchChannelId = twitchChannelId
        )

    async def __retrieveSessionToken(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        sessionToken = self.__cache.get(twitchChannelId, None)

        if utils.isValidStr(sessionToken):
            return sessionToken

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT sessiontoken FROM opentriviadatabasesessiontokens
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId
        )

        await connection.close()

        if record is not None and len(record) >= 1:
            sessionToken = record[0]

        self.__cache[twitchChannelId] = sessionToken

        return sessionToken

    async def __storeSessionToken(
        self,
        sessionToken: str | None,
        twitchChannelId: str
    ):
        if sessionToken is not None and not isinstance(sessionToken, str):
            raise TypeError(f'sessionToken argument is malformed: \"{sessionToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()

        if utils.isValidStr(sessionToken):
            await connection.execute(
                '''
                    INSERT INTO opentriviadatabasesessiontokens (sessiontoken, twitchchannelid)
                    VALUES ($1, $2)
                    ON CONFLICT (twitchchannelid) DO UPDATE SET sessiontoken = EXCLUDED.sessiontoken
                ''',
                sessionToken, twitchChannelId
            )

            self.__cache[twitchChannelId] = sessionToken
        else:
            await connection.execute(
                '''
                    DELETE FROM opentriviadatabasesessiontokens
                    WHERE twitchchannelid = $1
                ''',
                twitchChannelId
            )

            self.__cache.pop(twitchChannelId, None)

        await connection.close()
