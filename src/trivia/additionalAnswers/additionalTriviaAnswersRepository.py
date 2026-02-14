import traceback
from typing import Any

from frozenlist import FrozenList

from .additionalTriviaAnswer import AdditionalTriviaAnswer
from .additionalTriviaAnswers import AdditionalTriviaAnswers
from .additionalTriviaAnswersRepositoryInterface import AdditionalTriviaAnswersRepositoryInterface
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaExceptions import (AdditionalTriviaAnswerAlreadyExistsException,
                                AdditionalTriviaAnswerIsMalformedException,
                                AdditionalTriviaAnswerIsUnsupportedTriviaTypeException,
                                TooManyAdditionalTriviaAnswersException)
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...storage.exceptions import DatabaseOperationalError
from ...timber.timberInterface import TimberInterface
from ...twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class AdditionalTriviaAnswersRepository(AdditionalTriviaAnswersRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        triviaSettings: TriviaSettingsInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__triviaSettings: TriviaSettingsInterface = triviaSettings
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False

    async def addAdditionalTriviaAnswer(
        self,
        additionalAnswer: str,
        triviaId: str,
        userId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource,
    ) -> AdditionalTriviaAnswers:
        if not utils.isValidStr(additionalAnswer):
            raise AdditionalTriviaAnswerIsMalformedException(f'additionalAnswer argument is malformed: \"{additionalAnswer}\"')
        elif not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(triviaQuestionType, TriviaQuestionType):
            raise TypeError(f'triviaQuestionType argument is malformed: \"{triviaQuestionType}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        additionalAnswerLength = len(additionalAnswer)
        maxAdditionalTriviaAnswerLength = await self.__triviaSettings.getMaxAdditionalTriviaAnswerLength()

        if additionalAnswerLength > maxAdditionalTriviaAnswerLength:
            raise AdditionalTriviaAnswerIsMalformedException(f'Attempted to add additional answer \"{additionalAnswer}\" for {triviaSource.toStr()}:{triviaId}, but it is too long (len is {additionalAnswerLength}, max len is {maxAdditionalTriviaAnswerLength})')
        elif triviaQuestionType is not TriviaQuestionType.QUESTION_ANSWER:
            raise AdditionalTriviaAnswerIsUnsupportedTriviaTypeException(
                message = f'Attempted to add additional answer \"{additionalAnswer}\" for {triviaSource.toStr()}:{triviaId}, but it is an unsupported type ({triviaQuestionType=})',
                triviaQuestionType = triviaQuestionType,
                triviaSource = triviaSource,
            )

        reference = await self.getAdditionalTriviaAnswers(
            triviaId = triviaId,
            triviaQuestionType = triviaQuestionType,
            triviaSource = triviaSource,
        )

        additionalAnswersList: list[AdditionalTriviaAnswer] = list()

        if reference is not None:
            additionalAnswersList.extend(reference.answers)

            for existingAdditionalAnswer in reference.answerStrings:
                if existingAdditionalAnswer.casefold() == additionalAnswer.casefold():
                    raise AdditionalTriviaAnswerAlreadyExistsException(
                        message = f'Attempted to add additional answer \"{additionalAnswer}\" for {triviaSource.toStr()}:{triviaId}, but it already exists ({triviaQuestionType=}) ({reference=})',
                        triviaId = triviaId,
                        triviaQuestionType = triviaQuestionType,
                        triviaSource = triviaSource
                    )

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)

        userName = await self.__userIdsRepository.requireUserName(
            userId = userId,
            twitchAccessToken = twitchAccessToken,
        )

        additionalAnswersList.append(AdditionalTriviaAnswer(
            answer = additionalAnswer,
            userId = userId,
            userName = userName,
        ))

        additionalAnswersList.sort(key = lambda additionalAnswer: (additionalAnswer.answer.casefold(), additionalAnswer.userName.casefold()))

        if len(additionalAnswersList) > await self.__triviaSettings.getMaxAdditionalTriviaAnswers():
            raise TooManyAdditionalTriviaAnswersException(
                answerCount = len(additionalAnswersList),
                triviaId = triviaId,
                triviaQuestionType = triviaQuestionType,
                triviaSource = triviaSource,
            )

        connection = await self.__getDatabaseConnection()
        exception: DatabaseOperationalError | None = None

        try:
            await connection.execute(
                '''
                    INSERT INTO additionaltriviaanswers (additionalanswer, triviaid, triviasource, triviatype, userid)
                    VALUES ($1, $2, $3, $4, $5)
                ''',
                additionalAnswer, triviaId, triviaSource.toStr(), triviaQuestionType.toStr(), userId,
            )
        except DatabaseOperationalError as e:
            exception = e

        await connection.close()

        if exception is not None:
            self.__timber.log('AdditionalTriviaAnswersRepository', f'Encountered a database operational error when trying to insert additional trivia answer ({additionalAnswer=}) ({triviaId=}) ({triviaSource=}) ({triviaQuestionType=}): {exception}', exception, traceback.format_exc())

            raise AdditionalTriviaAnswerAlreadyExistsException(
                message = f'Attempted to add additional answer for {triviaSource.toStr()}:{triviaId}, but it already exists ({additionalAnswer=}) ({triviaQuestionType=}) ({additionalAnswersList=})',
                triviaId = triviaId,
                triviaQuestionType = triviaQuestionType,
                triviaSource = triviaSource,
            )

        self.__timber.log('AdditionalTriviaAnswersRepository', f'Added additional answer for {triviaSource.toStr()}:{triviaId} ({additionalAnswer=}) ({triviaQuestionType=}) ({additionalAnswersList=})')

        frozenAnswers: FrozenList[AdditionalTriviaAnswer] = FrozenList(additionalAnswersList)
        frozenAnswers.freeze()

        return AdditionalTriviaAnswers(
            answers = frozenAnswers,
            triviaId = triviaId,
            triviaQuestionType = triviaQuestionType,
            triviaSource = triviaSource,
        )

    async def addAdditionalTriviaAnswers(
        self,
        currentAnswers: list[str],
        triviaId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource,
    ) -> bool:
        if not isinstance(currentAnswers, list):
            raise TypeError(f'currentAnswers argument is malformed: \"{currentAnswers}\"')
        elif not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaQuestionType, TriviaQuestionType):
            raise TypeError(f'triviaQuestionType argument is malformed: \"{triviaQuestionType}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        reference = await self.getAdditionalTriviaAnswers(
            triviaId = triviaId,
            triviaQuestionType = triviaQuestionType,
            triviaSource = triviaSource
        )

        if reference is None:
            return False

        currentAnswers.extend(reference.answerStrings)
        return True

    async def deleteAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource,
    ) -> AdditionalTriviaAnswers | None:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaQuestionType, TriviaQuestionType):
            raise TypeError(f'triviaQuestionType argument is malformed: \"{triviaQuestionType}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        reference = await self.getAdditionalTriviaAnswers(
            triviaId = triviaId,
            triviaQuestionType = triviaQuestionType,
            triviaSource = triviaSource,
        )

        if reference is None:
            self.__timber.log('AdditionalTriviaAnswersRepository', f'Attempted to delete additional answers for {triviaSource.toStr()}:{triviaId}, but there were none ({reference=})')
            return None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM additionaltriviaanswers
                WHERE triviaid = $1 AND triviasource = $2 AND triviatype = $3
            ''',
            triviaId, triviaSource.toStr(), triviaQuestionType.toStr(),
        )

        await connection.close()
        self.__timber.log('AdditionalTriviaAnswersRepository', f'Deleted additional answers for {triviaSource.toStr()}:{triviaId} ({reference=})')

        return reference

    async def getAdditionalTriviaAnswers(
        self,
        triviaId: str,
        triviaQuestionType: TriviaQuestionType,
        triviaSource: TriviaSource,
    ) -> AdditionalTriviaAnswers | None:
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaQuestionType, TriviaQuestionType):
            raise TypeError(f'triviaQuestionType argument is malformed: \"{triviaQuestionType}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        if not await self.__triviaSettings.areAdditionalTriviaAnswersEnabled():
            return None

        connection = await self.__getDatabaseConnection()
        records: FrozenList[FrozenList[Any]] | None = None

        try:
            records = await connection.fetchRows(
                '''
                    SELECT additionaltriviaanswers.additionalanswer, additionaltriviaanswers.userid, userids.username FROM additionaltriviaanswers
                    INNER JOIN userids ON additionaltriviaanswers.userid = userids.userid
                    WHERE additionaltriviaanswers.triviaid = $1 AND additionaltriviaanswers.triviasource = $2 AND additionaltriviaanswers.triviatype = $3
                    ORDER BY additionaltriviaanswers.additionalanswer ASC
                ''',
                triviaId, triviaSource.toStr(), triviaQuestionType.toStr(),
            )
        except DatabaseOperationalError as e:
            self.__timber.log('AdditionalTriviaAnswersRepository', f'Encountered a database operational error when trying to retrieve additional trivia answers ({triviaId=}) ({triviaSource=}) ({triviaQuestionType=}): {e}', e, traceback.format_exc())

        await connection.close()

        if records is None or len(records) == 0:
            return None

        additionalAnswers: list[AdditionalTriviaAnswer] = list()

        for record in records:
            additionalAnswers.append(AdditionalTriviaAnswer(
                answer = record[0],
                userId = record[1],
                userName = record[2],
            ))

        additionalAnswers.sort(key = lambda additionalAnswer: (additionalAnswer.answer.casefold(), additionalAnswer.userName.casefold()))

        frozenAnswers: FrozenList[AdditionalTriviaAnswer] = FrozenList(additionalAnswers)
        frozenAnswers.freeze()

        return AdditionalTriviaAnswers(
            answers = frozenAnswers,
            triviaId = triviaId,
            triviaQuestionType = triviaQuestionType,
            triviaSource = triviaSource,
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS additionaltriviaanswers (
                            additionalanswer public.citext NOT NULL,
                            triviaid text NOT NULL,
                            triviasource text NOT NULL,
                            triviatype text NOT NULL,
                            userid text NOT NULL,
                            PRIMARY KEY (additionalanswer, triviaid, triviasource, triviatype)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS additionaltriviaanswers (
                            additionalanswer TEXT NOT NULL COLLATE NOCASE,
                            triviaid TEXT NOT NULL,
                            triviasource TEXT NOT NULL,
                            triviatype TEXT NOT NULL,
                            userid TEXT NOT NULL,
                            PRIMARY KEY (additionalanswer, triviaid, triviasource, triviatype)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
