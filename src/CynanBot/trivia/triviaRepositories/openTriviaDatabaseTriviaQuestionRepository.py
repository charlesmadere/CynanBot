import traceback
from typing import Any, Dict, List, Optional, Set

import CynanBot.misc.utils as utils
from CynanBot.misc.clearable import Clearable
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import (BadTriviaSessionTokenException,
                                              GenericTriviaNetworkException,
                                              MalformedTriviaJsonException,
                                              UnsupportedTriviaTypeException)
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


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

        assert isinstance(backingDatabase, BackingDatabase), f"malformed {backingDatabase=}"
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface), f"malformed {triviaQuestionCompiler=}"

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

        self.__isDatabaseReady: bool = False
        self.__cache: Dict[str, Optional[str]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', 'Caches cleared')

    async def __fetchNewSessionToken(self, twitchChannel: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Fetching new session token for \"{twitchChannel}\"...')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://opentdb.com/api_token.php?command=request')
        except GenericNetworkException as e:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Encountered network error when fetching Open Trivia Database\'s session token for twitchChannel: \"{twitchChannel}\": {e}', e, traceback.format_exc())
            raise BadTriviaSessionTokenException(f'Encountered network error when fetching Open Trivia Database\'s session token for twitchChannel: \"{twitchChannel}\": {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Encountered non-200 HTTP status code ({response.getStatusCode()}) when fetching Open Trivia Database\'s session token for twitchChannel: \"{twitchChannel}\"')
            raise BadTriviaSessionTokenException(f'Encountered non-200 HTTP status code ({response.getStatusCode()}) when fetching Open Trivia Database\'s session token for twitchChannel: \"{twitchChannel}\"')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'{jsonResponse}')

        if not utils.hasItems(jsonResponse):
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannel \"{twitchChannel}\" due to null/empty JSON contents: {jsonResponse}')
            raise BadTriviaSessionTokenException(f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannel \"{twitchChannel}\" due to null/empty JSON contents: {jsonResponse}')
        if utils.getIntFromDict(jsonResponse, 'response_code', fallback = -1) != 0:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannel \"{twitchChannel}\" due to bad \"response_code\" value: {jsonResponse}')
            raise BadTriviaSessionTokenException(f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannel \"{twitchChannel}\" due to bad \"response_code\" value: {jsonResponse}')
        if not utils.isValidStr(jsonResponse.get('token')):
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannel \"{twitchChannel}\" due to bad \"token\" value: {jsonResponse}')
            raise BadTriviaSessionTokenException(f'Rejecting Open Trivia Database\'s session token JSON data for twitchChannel \"{twitchChannel}\" due to bad \"token\" value: {jsonResponse}')

        return utils.getStrFromDict(jsonResponse, 'token')

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

        self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        sessionToken = await self.__getOrFetchNewSessionToken(fetchOptions.getTwitchChannel())
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

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'{jsonResponse}')

        if not utils.hasItems(jsonResponse):
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s JSON data due to null/empty JSON contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Open Trivia Database\'s JSON data due to null/empty JSON contents: {jsonResponse}')
        if utils.getIntFromDict(jsonResponse, 'response_code', fallback = -1) != 0:
            await self.__removeSessionToken(fetchOptions.getTwitchChannel())
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s JSON data due to bad \"response_code\" value: {jsonResponse}')
            raise GenericTriviaNetworkException(self.getTriviaSource())
        if not utils.hasItems(jsonResponse.get('results')):
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s JSON data due to missing/null/empty \"results\" array: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Open Trivia Database\'s JSON data due to missing/null/empty \"results\" array: {jsonResponse}')

        triviaJson: Optional[Dict[str, Any]] = jsonResponse['results'][0]

        if not utils.hasItems(triviaJson):
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Rejecting Open Trivia Database\'s JSON data due to null/empty \"results\" contents: {jsonResponse}')
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
            correctAnswerStrings: List[str] = list()
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
                    triviaSource = TriviaSource.OPEN_TRIVIA_DATABASE
                )
            else:
                self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', 'Encountered a multiple choice question that is better suited for true/false')
                triviaType = TriviaQuestionType.TRUE_FALSE

        if triviaType is TriviaQuestionType.TRUE_FALSE:
            correctAnswer = utils.getBoolFromDict(triviaJson, 'correct_answer')
            correctAnswerBools: List[bool] = list()
            correctAnswerBools.append(correctAnswer)

            return TrueFalseTriviaQuestion(
                correctAnswers = correctAnswerBools,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                triviaSource = TriviaSource.OPEN_TRIVIA_DATABASE
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Open Trivia Database: {jsonResponse}')

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __getOrFetchNewSessionToken(self, twitchChannel: str) -> Optional[str]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        sessionToken = await self.__retrieveSessionToken(twitchChannel)

        if not utils.isValidStr(sessionToken):
            try:
                sessionToken = await self.__fetchNewSessionToken(twitchChannel)
            except BadTriviaSessionTokenException:
                pass

        await self.__storeSessionToken(
            sessionToken = sessionToken,
            twitchChannel = twitchChannel
        )

        return sessionToken

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
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
                        twitchchannel public.citext NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS opentriviadatabasesessiontokens (
                        sessiontoken TEXT DEFAULT NULL,
                        twitchchannel TEXT NOT NULL PRIMARY KEY COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def __removeSessionToken(self, twitchChannel: str):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.__storeSessionToken(
            sessionToken = None,
            twitchChannel = twitchChannel
        )

    async def __retrieveSessionToken(self, twitchChannel: str) -> Optional[str]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        sessionToken = self.__cache.get(twitchChannel.lower())

        if utils.isValidStr(sessionToken):
            return sessionToken

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT sessiontoken FROM opentriviadatabasesessiontokens
                WHERE twitchchannel = $1
                LIMIT 1
            ''',
            twitchChannel
        )

        await connection.close()

        if utils.hasItems(record):
            sessionToken = record[0]

        self.__cache[twitchChannel.lower()] = sessionToken

        return sessionToken

    async def __storeSessionToken(
        self,
        sessionToken: Optional[str],
        twitchChannel: str
    ):
        assert sessionToken is None or isinstance(sessionToken, str), f"malformed {sessionToken=}"
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        connection = await self.__getDatabaseConnection()

        if utils.isValidStr(sessionToken):
            await connection.execute(
                '''
                    INSERT INTO opentriviadatabasesessiontokens (sessiontoken, twitchchannel)
                    VALUES ($1, $2)
                    ON CONFLICT (twitchchannel) DO UPDATE SET sessiontoken = EXCLUDED.sessiontoken
                ''',
                sessionToken, twitchChannel
            )

            self.__cache[twitchChannel.lower()] = sessionToken
        else:
            await connection.execute(
                '''
                    DELETE FROM opentriviadatabasesessiontokens
                    WHERE twitchchannel = $1
                ''',
                twitchChannel
            )

            self.__cache.pop(twitchChannel.lower(), None)

        await connection.close()
