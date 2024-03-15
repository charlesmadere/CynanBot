from typing import Any, List, Optional
import traceback

import CynanBot.misc.utils as utils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswer import \
    AdditionalTriviaAnswer
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswers import \
    AdditionalTriviaAnswers
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaExceptions import (
    AdditionalTriviaAnswerAlreadyExistsException,
    AdditionalTriviaAnswerIsMalformedException,
    AdditionalTriviaAnswerIsUnsupportedTriviaTypeException,
    TooManyAdditionalTriviaAnswersException)
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.storage.exceptions import DatabaseOperationalError


class AdditionalTriviaAnswersRepository(AdditionalTriviaAnswersRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise ValueError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise ValueError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False

    async def addAdditionalTriviaAnswer(
        self,
        additionalAnswer: str,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ) -> AdditionalTriviaAnswers:
        if not utils.isValidStr(additionalAnswer):
            raise AdditionalTriviaAnswerIsMalformedException(f'additionalAnswer argument is malformed: \"{additionalAnswer}\"')
        elif not utils.isValidStr(triviaId):
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise ValueError(f'triviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaType, TriviaQuestionType):
            raise ValueError(f'triviaType argument is malformed: \"{triviaType}\"')

        additionalAnswerLength = len(additionalAnswer)
        maxAdditionalTriviaAnswerLength = await self.__triviaSettingsRepository.getMaxAdditionalTriviaAnswerLength()

        if additionalAnswerLength > maxAdditionalTriviaAnswerLength:
            raise AdditionalTriviaAnswerIsMalformedException(f'Attempted to add additional answer \"{additionalAnswer}\" for {triviaSource.toStr()}:{triviaId}, but it is too long (len is {additionalAnswerLength}, max len is {maxAdditionalTriviaAnswerLength})')

        if triviaType is not TriviaQuestionType.QUESTION_ANSWER:
            raise AdditionalTriviaAnswerIsUnsupportedTriviaTypeException(
                message = f'Attempted to add additional answer \"{additionalAnswer}\" for {triviaSource.toStr()}:{triviaId}, but it is an unsupported type ({triviaType.toStr})',
                triviaSource = triviaSource,
                triviaType = triviaType
            )

        reference = await self.getAdditionalTriviaAnswers(
            triviaId = triviaId,
            triviaSource = triviaSource,
            triviaType = triviaType
        )

        additionalAnswersList: List[AdditionalTriviaAnswer] = list()

        if reference is not None:
            additionalAnswersList.extend(reference.getAdditionalAnswers())

            for existingAdditionalAnswer in reference.getAdditionalAnswersStrs():
                if existingAdditionalAnswer.lower() == additionalAnswer.lower():
                    raise AdditionalTriviaAnswerAlreadyExistsException(
                        message = f'Attempted to add additional answer \"{additionalAnswer}\" for {triviaSource.toStr()}:{triviaId}, but it already exists',
                        triviaId = triviaId,
                        triviaSource = triviaSource,
                        triviaType = triviaType
                    )

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)
        userName = await self.__userIdsRepository.requireUserName(
            userId = userId,
            twitchAccessToken = twitchAccessToken
        )

        additionalAnswersList.append(AdditionalTriviaAnswer(
            additionalAnswer = additionalAnswer,
            userId = userId,
            userName = userName
        ))

        if len(additionalAnswersList) > await self.__triviaSettingsRepository.getMaxAdditionalTriviaAnswers():
            raise TooManyAdditionalTriviaAnswersException(
                answerCount = len(additionalAnswersList),
                triviaId = triviaId,
                triviaSource = triviaSource,
                triviaType = triviaType
            )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO additionaltriviaanswers (additionalanswer, triviaid, triviasource, triviatype, userid)
                VALUES ($1, $2, $3, $4, $5)
            ''',
            additionalAnswer, triviaId, triviaSource.toStr(), triviaType.toStr(), userId
        )

        await connection.close()
        self.__timber.log('AdditionalTriviaAnswersRepository', f'Added additional answer (\"{additionalAnswer}\") for {triviaSource.toStr()}:{triviaId}, all answers: {additionalAnswersList}')

        return AdditionalTriviaAnswers(
            additionalAnswers = additionalAnswersList,
            triviaId = triviaId,
            triviaSource = triviaSource,
            triviaType = triviaType
        )

    async def addAdditionalTriviaAnswers(
        self,
        currentAnswers: List[str],
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ) -> bool:
        if not isinstance(currentAnswers, List):
            raise ValueError(f'currentAnswers argument is malformed: \"{currentAnswers}\"')
        elif not utils.isValidStr(triviaId):
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise ValueError(f'triviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaType, TriviaQuestionType):
            raise ValueError(f'triviaType argument is malformed: \"{triviaType}\"')

        reference = await self.getAdditionalTriviaAnswers(
            triviaId = triviaId,
            triviaSource = triviaSource,
            triviaType = triviaType
        )

        if reference is None:
            return False

        currentAnswers.extend(reference.getAdditionalAnswersStrs())
        return True

    async def deleteAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ) -> Optional[AdditionalTriviaAnswers]:
        if not utils.isValidStr(triviaId):
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise ValueError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        reference = await self.getAdditionalTriviaAnswers(
            triviaId = triviaId,
            triviaSource = triviaSource,
            triviaType = triviaType
        )

        if reference is None:
            self.__timber.log('AdditionalTriviaAnswersRepository', f'Attempted to delete additional answers for {triviaSource.toStr()}:{triviaId}, but there were none')
            return None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM additionaltriviaanswers
                WHERE triviaid = $1 AND triviasource = $2 AND triviatype = $3
            ''',
            triviaId, triviaSource.toStr(), triviaType.toStr()
        )

        await connection.close()
        self.__timber.log('AdditionalTriviaAnswersRepository', f'Deleted additional answers for {triviaSource.toStr()}:{triviaId} (existing additional answers were {reference.getAdditionalAnswers()})')

        return reference

    async def getAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ) -> Optional[AdditionalTriviaAnswers]:
        if not utils.isValidStr(triviaId):
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise ValueError(f'triviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaType, TriviaQuestionType):
            raise ValueError(f'triviaType argument is malformed: \"{triviaType}\"')

        if not await self.__triviaSettingsRepository.areAdditionalTriviaAnswersEnabled():
            return None

        connection = await self.__getDatabaseConnection()
        records: Optional[List[List[Any]]] = None

        try:
            records = await connection.fetchRows(
                '''
                    SELECT additionaltriviaanswers.additionalanswer, additionaltriviaanswers.userid, userids.username FROM additionaltriviaanswers
                    INNER JOIN userids ON additionaltriviaanswers.userid = userids.userid
                    WHERE additionaltriviaanswers.triviaid = $1 AND additionaltriviaanswers.triviasource = $2 AND additionaltriviaanswers.triviatype = $3
                    ORDER BY additionaltriviaanswers.additionalanswer ASC
                ''',
                triviaId, triviaSource.toStr(), triviaType.toStr()
            )
        except DatabaseOperationalError as e:
            self.__timber.log('AdditionalTriviaAnswersRepository', f'Encountered a database operational error when trying to retrieve additional trivia answers ({triviaId=}) ({triviaSource=}) ({triviaType=}): {e}', e, traceback.format_exc())

        await connection.close()

        if records is None or len(records) == 0:
            return None

        additionalAnswers: List[AdditionalTriviaAnswer] = list()

        for record in records:
            additionalAnswers.append(AdditionalTriviaAnswer(
                additionalAnswer = record[0],
                userId = record[1],
                userName = record[2]
            ))

        additionalAnswers.sort(key = lambda additionalAnswer: (additionalAnswer.getAdditionalAnswer().lower(), additionalAnswer.getUserId().lower()))

        return AdditionalTriviaAnswers(
            additionalAnswers = additionalAnswers,
            triviaId = triviaId,
            triviaSource = triviaSource,
            triviaType = triviaType
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS additionaltriviaanswers (
                        additionalanswer text NOT NULL,
                        triviaid public.citext NOT NULL,
                        triviasource public.citext NOT NULL,
                        triviatype public.citext NOT NULL,
                        userid public.citext NOT NULL
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS additionaltriviaanswers (
                        additionalanswer TEXT NOT NULL,
                        triviaid TEXT NOT NULL COLLATE NOCASE,
                        triviasource TEXT NOT NULL COLLATE NOCASE,
                        triviatype TEXT NOT NULL COLLATE NOCASE,
                        userid TEXT NOT NULL COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
