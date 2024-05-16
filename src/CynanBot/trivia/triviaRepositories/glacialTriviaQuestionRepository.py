import traceback

import aiofiles
import aiofiles.ospath
import aiosqlite
from aiosqlite import Connection

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import (
    BadTriviaTypeException, NoTriviaCorrectAnswersException,
    NoTriviaMultipleChoiceResponsesException, UnsupportedTriviaTypeException)
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class GlacialTriviaQuestionRepository(
    AbsTriviaQuestionRepository,
    GlacialTriviaQuestionRepositoryInterface
):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        triviaDatabaseFile: str = 'glacialTriviaQuestionsDatabase.sqlite'
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface):
            raise TypeError(f'triviaAnswerCompiler argument is malformed: \"{triviaAnswerCompiler}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidStr(triviaDatabaseFile):
            raise TypeError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__areTablesCreated: bool = False
        self.__hasQuestionSetAvailable: bool | None = None
        self.__twitchChannelId: str | None = None

    async def __buildCleanedCorrectAnswersForQuestionAnswerTrivia(
        self,
        correctAnswers: list[str]
    ) -> list[str]:
        cleanedCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(correctAnswers)

        expandedCleanedCorrectAnswers: set[str] = set()
        for answer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.__triviaAnswerCompiler.expandNumerals(answer))

        return list(expandedCleanedCorrectAnswers)

    async def __checkIfQuestionIsAlreadyStored(
        self,
        question: AbsTriviaQuestion,
        connection: Connection
    ) -> bool:
        cursor = await connection.execute(
            '''
                SELECT EXISTS(
                    SELECT 1 FROM glacialQuestions
                    WHERE originalTriviaSource = $1 AND triviaId = $2
                    LIMIT 1
                )
            ''',
            (question.getTriviaSource().toStr(), question.getTriviaId(), )
        )

        row = await cursor.fetchone()
        await cursor.close()

        return row is not None and len(row) >= 1 and row[0] == 1

    async def __createTablesIfNotExists(self, connection: Connection):
        if self.__areTablesCreated:
            return

        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS glacialQuestions (
                    category TEXT DEFAULT NULL COLLATE NOCASE,
                    categoryId TEXT DEFAULT NULL COLLATE NOCASE,
                    originalTriviaSource TEXT NOT NULL COLLATE NOCASE,
                    question TEXT NOT NULL COLLATE NOCASE,
                    triviaDifficulty TEXT NOT NULL COLLATE NOCASE,
                    triviaId TEXT NOT NULL COLLATE NOCASE,
                    triviaType TEXT NOT NULL COLLATE NOCASE,
                    PRIMARY KEY (originalTriviaSource, triviaId)
                )
            '''
        )
        await cursor.close()

        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS glacialAnswers (
                    answer TEXT NOT NULL COLLATE NOCASE,
                    originalTriviaSource TEXT NOT NULL COLLATE NOCASE,
                    triviaId TEXT NOT NULL COLLATE NOCASE
                )
            '''
        )
        await cursor.close()

        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS glacialResponses (
                    response TEXT NOT NULL COLLATE NOCASE,
                    originalTriviaSource TEXT NOT NULL COLLATE NOCASE,
                    triviaId TEXT NOT NULL COLLATE NOCASE
                )
            '''
        )
        await cursor.close()

        self.__areTablesCreated = True

    async def __triviaDatabaseFileExists(self) -> bool:
        return await aiofiles.ospath.exists(self.__triviaDatabaseFile)

    async def __fetchAnyTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions
    ) -> AbsTriviaQuestion | None:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT category, categoryId, originalTriviaSource, question, triviaDifficulty, triviaId, triviaType FROM glacialQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        await cursor.close()

        if row is None or len(row) == 0:
            await connection.close()
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any trivia question in the database! ({fetchOptions=})')
            return None

        category = await self.__triviaQuestionCompiler.compileCategory(row[0])
        categoryId: str | None = row[1]
        originalTriviaSource = TriviaSource.fromStr(row[2])
        question = await self.__triviaQuestionCompiler.compileQuestion(row[3])
        triviaDifficulty = TriviaDifficulty.fromStr(row[4])
        triviaId: str = row[5]
        triviaType = TriviaQuestionType.fromStr(row[6])

        correctAnswers = await self.__fetchTriviaQuestionCorrectAnswers(
            connection = connection,
            triviaId = triviaId,
            triviaType = triviaType,
            originalTriviaSource = originalTriviaSource,
        )

        multipleChoiceResponses: list[str] | None = None

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            multipleChoiceResponses = await self.__fetchTriviaQuestionMultipleChoiceResponses(
                connection = connection,
                triviaId = triviaId,
                originalTriviaSource = originalTriviaSource
            )

            await connection.close()

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = categoryId,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = originalTriviaSource,
                triviaSource = self.getTriviaSource()
            )
        elif triviaType is TriviaQuestionType.QUESTION_ANSWER:
            await connection.close()
            cleanedCorrectAnswers = await self.__buildCleanedCorrectAnswersForQuestionAnswerTrivia(correctAnswers)

            return QuestionAnswerTriviaQuestion(
                correctAnswers = correctAnswers,
                cleanedCorrectAnswers = cleanedCorrectAnswers,
                category = category,
                categoryId = categoryId,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = originalTriviaSource,
                triviaSource = self.getTriviaSource()
            )
        elif triviaType is TriviaQuestionType.TRUE_FALSE:
            await connection.close()

            return TrueFalseTriviaQuestion(
                correctAnswers = utils.strsToBools(correctAnswers),
                category = category,
                categoryId = categoryId,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = originalTriviaSource,
                triviaSource = self.getTriviaSource()
            )
        else:
            exception = UnsupportedTriviaTypeException(f'Received an invalid trivia question type! ({triviaType=}) ({fetchOptions=}) ({row=})')
            self.__timber.log('GlacialTriviaQuestionRepository', f'Received an invalid trivia question type when fetching a question answer trivia question ({triviaType=}) ({fetchOptions=}) ({row=}): {exception}', exception, traceback.format_exc())
            raise exception

    async def __fetchMultipleChoiceOrTrueFalseTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions
    ) -> AbsTriviaQuestion | None:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT category, categoryId, originalTriviaSource, question, triviaDifficulty, triviaId, triviaType FROM glacialQuestions
                WHERE triviaType = $1 OR triviaType = $2
                ORDER BY RANDOM()
                LIMIT 1
            ''',
            (TriviaQuestionType.MULTIPLE_CHOICE.toStr(), TriviaQuestionType.TRUE_FALSE.toStr(), )
        )

        row = await cursor.fetchone()
        await cursor.close()

        if row is None or len(row) == 0:
            await connection.close()
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any {TriviaQuestionType.MULTIPLE_CHOICE} or {TriviaQuestionType.TRUE_FALSE} question in the database! ({fetchOptions=})')
            return None

        category = await self.__triviaQuestionCompiler.compileCategory(row[0])
        categoryId: str | None = row[1]
        originalTriviaSource = TriviaSource.fromStr(row[2])
        question = await self.__triviaQuestionCompiler.compileQuestion(row[3])
        triviaDifficulty = TriviaDifficulty.fromStr(row[4])
        triviaId: str = row[5]
        triviaType = TriviaQuestionType.fromStr(row[6])

        correctAnswers = await self.__fetchTriviaQuestionCorrectAnswers(
            connection = connection,
            triviaId = triviaId,
            triviaType = triviaType,
            originalTriviaSource = originalTriviaSource
        )

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            multipleChoiceResponses = await self.__fetchTriviaQuestionMultipleChoiceResponses(
                connection = connection,
                triviaId = triviaId,
                originalTriviaSource = originalTriviaSource
            )

            await connection.close()

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = categoryId,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = originalTriviaSource,
                triviaSource = self.getTriviaSource()
            )
        elif triviaType is TriviaQuestionType.TRUE_FALSE:
            await connection.close()

            return TrueFalseTriviaQuestion(
                correctAnswers = utils.strsToBools(correctAnswers),
                category = category,
                categoryId = categoryId,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = originalTriviaSource,
                triviaSource = self.getTriviaSource()
            )
        else:
            await connection.close()
            exception = UnsupportedTriviaTypeException(f'Received an invalid trivia question type! ({triviaType=}) ({fetchOptions=}) ({row=})')
            self.__timber.log('GlacialTriviaQuestionRepository', f'Received an invalid trivia question type when fetching a multiple choice or true false trivia question ({triviaType=}) ({fetchOptions=}) ({row=}): {exception}', exception, traceback.format_exc())
            raise exception

    async def __fetchQuestionAnswerTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions
    ) -> QuestionAnswerTriviaQuestion | None:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT category, categoryId, originalTriviaSource, question, triviaDifficulty, triviaId FROM glacialQuestions
                WHERE triviaType = $1
                ORDER BY RANDOM()
                LIMIT 1
            ''',
            (TriviaQuestionType.QUESTION_ANSWER.toStr(), )
        )

        row = await cursor.fetchone()
        await cursor.close()

        if row is None or len(row) == 0:
            await connection.close()
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any {TriviaQuestionType.QUESTION_ANSWER} question in the database! ({fetchOptions=})')
            return None

        category = await self.__triviaQuestionCompiler.compileCategory(row[0])
        categoryId: str | None = row[1]
        originalTriviaSource = TriviaSource.fromStr(row[2])
        question = await self.__triviaQuestionCompiler.compileQuestion(row[3])
        triviaDifficulty = TriviaDifficulty.fromStr(row[4])
        triviaId: str = row[5]

        correctAnswers = await self.__fetchTriviaQuestionCorrectAnswers(
            connection = connection,
            triviaId = triviaId,
            triviaType = TriviaQuestionType.QUESTION_ANSWER,
            originalTriviaSource = originalTriviaSource
        )

        await connection.close()
        cleanedCorrectAnswers = await self.__buildCleanedCorrectAnswersForQuestionAnswerTrivia(correctAnswers)

        return QuestionAnswerTriviaQuestion(
            correctAnswers = correctAnswers,
            cleanedCorrectAnswers = cleanedCorrectAnswers,
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = triviaDifficulty,
            originalTriviaSource = originalTriviaSource,
            triviaSource = self.getTriviaSource()
        )

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        if not await self.__triviaDatabaseFileExists():
            raise FileNotFoundError(f'Glacial trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        question: AbsTriviaQuestion | None = None

        if fetchOptions.requireQuestionAnswerTriviaQuestion():
            question = await self.__fetchQuestionAnswerTriviaQuestion(fetchOptions)
        elif fetchOptions.areQuestionAnswerTriviaQuestionsEnabled():
            question = await self.__fetchAnyTriviaQuestion(fetchOptions)
        else:
            question = await self.__fetchMultipleChoiceOrTrueFalseTriviaQuestion(fetchOptions)

        if not isinstance(question, AbsTriviaQuestion):
            raise RuntimeError('not yet implemented')

        return question

    async def __fetchTriviaQuestionCorrectAnswers(
        self,
        connection: Connection,
        triviaId: str,
        triviaType: TriviaQuestionType,
        originalTriviaSource: TriviaSource
    ) -> list[str]:
        cursor = await connection.execute(
            '''
                SELECT answer FROM glacialAnswers
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, )
        )

        rows = await cursor.fetchall()
        await cursor.close()
        correctAnswersSet: set[str] = set()

        if rows is not None:
            for row in rows:
                correctAnswersSet.add(row[0])

        if len(correctAnswersSet) == 0:
            await connection.close()
            exception = NoTriviaCorrectAnswersException(f'No trivia answers found! ({triviaId=}) ({originalTriviaSource=})')
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any trivia answers for {triviaId=} and {originalTriviaSource=}: {exception}', exception, traceback.format_exc())
            raise exception

        correctAnswers = list(correctAnswersSet)

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = correctAnswers,
            triviaId = triviaId,
            triviaSource = self.getTriviaSource(),
            triviaType = triviaType
        ):
            self.__timber.log('GlacialTriviaQuestionRepository', f'Added additional answers to question ({triviaId=})')

        return correctAnswers

    async def __fetchTriviaQuestionMultipleChoiceResponses(
        self,
        connection: Connection,
        triviaId: str,
        originalTriviaSource: TriviaSource
    ) -> list[str]:
        cursor = await connection.execute(
            '''
                SELECT response FROM glacialResponses
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, )
        )

        rows = await cursor.fetchall()
        await cursor.close()
        multipleChoiceResponses: set[str] = set()

        if rows is not None:
            for row in rows:
                multipleChoiceResponses.add(row[0])

        if len(multipleChoiceResponses) == 0:
            await connection.close()
            exception = NoTriviaMultipleChoiceResponsesException(f'No trivia responses found! ({triviaId=}) ({originalTriviaSource=})')
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any trivia responses for {triviaId=} and {originalTriviaSource=}: {exception}', exception, traceback.format_exc())
            raise exception

        return await self.__triviaQuestionCompiler.compileResponses(multipleChoiceResponses)

    def getSupportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return {
            TriviaQuestionType.MULTIPLE_CHOICE,
            TriviaQuestionType.QUESTION_ANSWER,
            TriviaQuestionType.TRUE_FALSE
        }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.GLACIAL

    async def __getTwitchChannelId(self) -> str:
        twitchChannelId = self.__twitchChannelId

        if twitchChannelId is not None:
            return twitchChannelId

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchChannelId = await self.__userIdsRepository.requireUserId(twitchHandle)
        self.__twitchChannelId = twitchChannelId

        return twitchChannelId

    async def hasQuestionSetAvailable(self) -> bool:
        hasQuestionSetAvailable = self.__hasQuestionSetAvailable

        if hasQuestionSetAvailable is not None:
            return hasQuestionSetAvailable

        hasQuestionSetAvailable = await self.__triviaDatabaseFileExists()

        if hasQuestionSetAvailable:
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle()
            twitchChannelId = await self.__getTwitchChannelId()

            multipleChoiceOrTrueFalse = await self.__fetchMultipleChoiceOrTrueFalseTriviaQuestion(TriviaFetchOptions(
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId,
                questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
            ))

            questionAnswer = await self.__fetchQuestionAnswerTriviaQuestion(TriviaFetchOptions(
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId,
                questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
            ))

            hasQuestionSetAvailable = multipleChoiceOrTrueFalse is not None and questionAnswer is not None

        self.__hasQuestionSetAvailable = hasQuestionSetAvailable
        return hasQuestionSetAvailable

    async def remove(self, triviaId: str, originalTriviaSource: TriviaSource):
        if not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(originalTriviaSource, TriviaSource):
            raise TypeError(f'originalTriviaSource argument is malformed: \"{originalTriviaSource}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)

        cursor = await connection.execute(
            '''
                DELETE FROM glacialAnswers
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, )
        )
        await cursor.close()

        cursor = await connection.execute(
            '''
                DELETE FROM glacialQuestions
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, )
        )
        await cursor.close()

        cursor = await connection.execute(
            '''
                DELETE FROM glacialResponses
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, )
        )
        await cursor.close()

        await connection.commit()
        await connection.close()
        self.__timber.log('GlacialTriviaQuestionRepository', f'Removed trivia question ({triviaId=}) ({originalTriviaSource=})')

    async def store(self, question: AbsTriviaQuestion) -> bool:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if not await self._triviaSettingsRepository.isScraperEnabled():
            return False

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        await self.__createTablesIfNotExists(connection)

        if await self.__checkIfQuestionIsAlreadyStored(
            question = question,
            connection = connection
        ):
            await connection.close()
            self.__timber.log('GlacialTriviaQuestionRepository', f'The given question already exists in the glacial trivia question database ({question=})')
            return False

        await self.__storeBaseTriviaQuestionData(
            question = question,
            connection = connection
        )

        if question.getTriviaType() is TriviaQuestionType.MULTIPLE_CHOICE and isinstance(question, MultipleChoiceTriviaQuestion):
            await self.__storeMultipleChoiceTriviaQuestion(
                connection = connection,
                question = question
            )
        elif question.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER and isinstance(question, QuestionAnswerTriviaQuestion):
            await self.__storeQuestionAnswerTriviaQuestion(
                connection = connection,
                question = question
            )
        elif question.getTriviaType() is TriviaQuestionType.TRUE_FALSE and isinstance(question, TrueFalseTriviaQuestion):
            await self.__storeTrueFalseTriviaQuestion(
                connection = connection,
                question = question
            )
        else:
            await connection.close()
            exception = BadTriviaTypeException(f'The given question is a confusing/malformed/misconstrued trivia type ({question=})')
            self.__timber.log('GlacialTriviaQuestionRepository', f'Attempted to store a trivia question, but it seems to be a broken trivia type ({question=}): {exception}', exception, traceback.format_exc())
            raise exception

        await connection.commit()
        await connection.close()
        self.__hasQuestionSetAvailable = None
        self.__timber.log('GlacialTriviaQuestionRepository', f'Added a new question into the glacial trivia question database ({question=})')
        return True

    async def __storeBaseTriviaQuestionData(
        self,
        question: AbsTriviaQuestion,
        connection: Connection
    ):
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(connection, Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')

        await connection.execute_insert(
            '''
                INSERT INTO glacialQuestions (category, categoryId, originalTriviaSource, question, triviaDifficulty, triviaId, triviaType)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            ''',
            (question.getCategory(), question.getCategoryId(), question.getTriviaSource().toStr(), question.getQuestion(), question.getTriviaDifficulty().toStr(), question.getTriviaId(), question.getTriviaType().toStr(), )
        )

    async def __storeMultipleChoiceTriviaQuestion(
        self,
        connection: Connection,
        question: MultipleChoiceTriviaQuestion
    ):
        if not isinstance(connection, Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')
        elif not isinstance(question, MultipleChoiceTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif question.getTriviaType() is not TriviaQuestionType.MULTIPLE_CHOICE:
            raise ValueError(f'question class and TriviaQuestionType do not match ({question=}) ({question.getTriviaType()=})')

        for answer in question.getRawCorrectAnswers():
            await connection.execute_insert(
                '''
                    INSERT INTO glacialAnswers (answer, originalTriviaSource, triviaId)
                    VALUES ($1, $2, $3)
                ''',
                (answer, question.getTriviaSource().toStr(), question.getTriviaId(), )
            )

        for response in question.getResponses():
            await connection.execute_insert(
                '''
                    INSERT INTO glacialResponses (response, originalTriviaSource, triviaId)
                    VALUES ($1, $2, $3)
                ''',
                (response, question.getTriviaSource().toStr(), question.getTriviaId(), )
            )

    async def __storeQuestionAnswerTriviaQuestion(
        self,
        connection: Connection,
        question: QuestionAnswerTriviaQuestion
    ):
        if not isinstance(connection, Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')
        elif not isinstance(question, QuestionAnswerTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif question.getTriviaType() is not TriviaQuestionType.QUESTION_ANSWER:
            raise ValueError(f'question class and TriviaQuestionType do not match ({question=}) ({question.getTriviaType()=})')

        for answer in question.getCorrectAnswers():
            await connection.execute_insert(
                '''
                    INSERT INTO glacialAnswers (answer, originalTriviaSource, triviaId)
                    VALUES ($1, $2, $3)
                ''',
                (answer, question.getTriviaSource().toStr(), question.getTriviaId(), )
            )

    async def __storeTrueFalseTriviaQuestion(
        self,
        connection: Connection,
        question: TrueFalseTriviaQuestion
    ):
        if not isinstance(connection, Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')
        elif not isinstance(question, TrueFalseTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif question.getTriviaType() is not TriviaQuestionType.TRUE_FALSE:
            raise ValueError(f'question class and TriviaQuestionType do not match ({question=}) ({question.getTriviaType()=})')

        for answer in question.getCorrectAnswerBools():
            await connection.execute_insert(
                '''
                    INSERT INTO glacialAnswers (answer, originalTriviaSource, triviaId)
                    VALUES ($1, $2, $3)
                ''',
                (str(answer), question.getTriviaSource().toStr(), question.getTriviaId(), )
            )
