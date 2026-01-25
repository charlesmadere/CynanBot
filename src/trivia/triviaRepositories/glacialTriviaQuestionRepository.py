import traceback
from typing import Final

import aiofiles
import aiofiles.ospath
import aiosqlite
from aiosqlite import Connection
from frozenlist import FrozenList

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .glacialTriviaQuestionRepositoryInterface import GlacialTriviaQuestionRepositoryInterface
from ..additionalAnswers.additionalTriviaAnswersRepositoryInterface import AdditionalTriviaAnswersRepositoryInterface
from ..compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..misc.triviaSourceParserInterface import TriviaSourceParserInterface
from ..questionAnswerTriviaConditions import QuestionAnswerTriviaConditions
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import (BadTriviaTypeException,
                                NoTriviaCorrectAnswersException,
                                NoTriviaMultipleChoiceResponsesException,
                                NoTriviaQuestionException,
                                UnsupportedTriviaTypeException)
from ..triviaFetchOptions import TriviaFetchOptions
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class GlacialTriviaQuestionRepository(
    AbsTriviaQuestionRepository,
    GlacialTriviaQuestionRepositoryInterface,
):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaSourceParser: TriviaSourceParserInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        triviaDatabaseFile: str = '../db/glacialTriviaQuestionsDatabase.sqlite',
    ):
        super().__init__(
            triviaSettingsRepository = triviaSettingsRepository,
        )

        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface):
            raise TypeError(f'triviaAnswerCompiler argument is malformed: \"{triviaAnswerCompiler}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')
        elif not isinstance(triviaSourceParser, TriviaSourceParserInterface):
            raise TypeError(f'triviaSourceParser argument is malformed: \"{triviaSourceParser}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidStr(triviaDatabaseFile):
            raise TypeError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__additionalTriviaAnswersRepository: Final[AdditionalTriviaAnswersRepositoryInterface] = additionalTriviaAnswersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaAnswerCompiler: Final[TriviaAnswerCompilerInterface] = triviaAnswerCompiler
        self.__triviaQuestionCompiler: Final[TriviaQuestionCompilerInterface] = triviaQuestionCompiler
        self.__triviaSourceParser: Final[TriviaSourceParserInterface] = triviaSourceParser
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__triviaDatabaseFile: Final[str] = triviaDatabaseFile

        self.__areTablesCreated: bool = False
        self.__hasQuestionSetAvailable: bool | None = None
        self.__twitchChannelId: str | None = None

    async def __buildCompiledCorrectAnswersForQuestionAnswerTrivia(
        self,
        correctAnswers: list[str],
    ) -> list[str]:
        compiledCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(correctAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for answer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.__triviaAnswerCompiler.expandNumerals(answer))

        return list(expandedCompiledCorrectAnswers)

    async def __checkIfQuestionIsAlreadyStored(
        self,
        question: AbsTriviaQuestion,
        connection: Connection,
    ) -> bool:
        cursor = await connection.execute(
            '''
                SELECT EXISTS(
                    SELECT 1 FROM glacialQuestions
                    WHERE originalTriviaSource = $1 AND triviaId = $2
                    LIMIT 1
                )
            ''',
            (question.triviaSource.toStr(), question.triviaId, ),
        )

        row = await cursor.fetchone()
        await cursor.close()

        return row is not None and len(row) >= 1 and utils.isValidInt(row[0]) and row[0] == 1

    async def __createTablesIfNotExists(self, connection: Connection):
        if self.__areTablesCreated:
            return

        self.__areTablesCreated = True

        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS glacialQuestions (
                    category TEXT DEFAULT NULL COLLATE NOCASE,
                    categoryId TEXT DEFAULT NULL,
                    originalTriviaSource TEXT NOT NULL,
                    question TEXT NOT NULL COLLATE NOCASE,
                    triviaDifficulty TEXT NOT NULL,
                    triviaId TEXT NOT NULL,
                    triviaType TEXT NOT NULL,
                    PRIMARY KEY (originalTriviaSource, triviaId)
                ) STRICT
            '''
        )
        await cursor.close()

        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS glacialAnswers (
                    answer TEXT NOT NULL COLLATE NOCASE,
                    originalTriviaSource TEXT NOT NULL,
                    triviaId TEXT NOT NULL
                ) STRICT
            '''
        )
        await cursor.close()

        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS glacialResponses (
                    response TEXT NOT NULL COLLATE NOCASE,
                    originalTriviaSource TEXT NOT NULL,
                    triviaId TEXT NOT NULL
                ) STRICT
            '''
        )
        await cursor.close()

    async def __triviaDatabaseFileExists(self) -> bool:
        return await aiofiles.ospath.exists(self.__triviaDatabaseFile)

    async def __fetchAllQuestionAnswerTriviaQuestions(
        self,
        fetchOptions: TriviaFetchOptions,
    ) -> FrozenList[QuestionAnswerTriviaQuestion] | None:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT category, categoryId, originalTriviaSource, question, triviaDifficulty, triviaId FROM glacialQuestions
                WHERE triviaType = $1
            ''',
            (TriviaQuestionType.QUESTION_ANSWER.toStr(), )
        )

        rows = await cursor.fetchall()
        await cursor.close()

        if rows is None or sum(1 for _ in rows) == 0:
            await connection.close()
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any {TriviaQuestionType.QUESTION_ANSWER} questions in the database! ({fetchOptions=})')
            return None

        questions: FrozenList[QuestionAnswerTriviaQuestion] = FrozenList()

        for row in rows:
            category = await self.__triviaQuestionCompiler.compileCategory(row[0])
            categoryId: str | None = row[1]
            originalTriviaSource = await self.__triviaSourceParser.parse(row[2])
            question = await self.__triviaQuestionCompiler.compileQuestion(row[3])
            triviaDifficulty = TriviaDifficulty.fromStr(row[4])
            triviaId: str = row[5]

            originalCorrectAnswers = await self.__fetchTriviaQuestionCorrectAnswers(
                connection = connection,
                triviaId = triviaId,
                triviaType = TriviaQuestionType.QUESTION_ANSWER,
                originalTriviaSource = originalTriviaSource,
            )

            correctAnswers = await self.__triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
            compiledCorrectAnswers = await self.__buildCompiledCorrectAnswersForQuestionAnswerTrivia(originalCorrectAnswers)

            questions.append(QuestionAnswerTriviaQuestion(
                allWords = None,
                compiledCorrectAnswers = compiledCorrectAnswers,
                correctAnswers = correctAnswers,
                originalCorrectAnswers = originalCorrectAnswers,
                category = category,
                categoryId = categoryId,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = originalTriviaSource,
                triviaSource = self.triviaSource,
            ))

        await connection.close()
        questions.freeze()

        return questions

    async def __fetchAnyTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions,
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
        originalTriviaSource = await self.__triviaSourceParser.parse(row[2])
        question = await self.__triviaQuestionCompiler.compileQuestion(row[3])
        triviaDifficulty = TriviaDifficulty.fromStr(row[4])
        triviaId: str = row[5]
        triviaType = TriviaQuestionType.fromStr(row[6])

        originalCorrectAnswers = await self.__fetchTriviaQuestionCorrectAnswers(
            connection = connection,
            triviaId = triviaId,
            triviaType = triviaType,
            originalTriviaSource = originalTriviaSource,
        )

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(originalCorrectAnswers)

        match triviaType:
            case TriviaQuestionType.MULTIPLE_CHOICE:
                multipleChoiceResponses = await self.__fetchTriviaQuestionMultipleChoiceResponses(
                    connection = connection,
                    triviaId = triviaId,
                    originalTriviaSource = originalTriviaSource,
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
                    triviaSource = self.triviaSource,
                )

            case TriviaQuestionType.QUESTION_ANSWER:
                await connection.close()
                compiledCorrectAnswers = await self.__buildCompiledCorrectAnswersForQuestionAnswerTrivia(originalCorrectAnswers)

                return QuestionAnswerTriviaQuestion(
                    allWords = None,
                    compiledCorrectAnswers = compiledCorrectAnswers,
                    correctAnswers = correctAnswers,
                    originalCorrectAnswers = originalCorrectAnswers,
                    category = category,
                    categoryId = categoryId,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = originalTriviaSource,
                    triviaSource = self.triviaSource,
                )

            case TriviaQuestionType.TRUE_FALSE:
                await connection.close()

                return TrueFalseTriviaQuestion(
                    correctAnswer = utils.strictStrToBool(originalCorrectAnswers[0]),
                    category = category,
                    categoryId = categoryId,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = originalTriviaSource,
                    triviaSource = self.triviaSource,
                )

            case _:
                exception = UnsupportedTriviaTypeException(f'Received an invalid trivia question type! ({triviaType=}) ({fetchOptions=}) ({row=})')
                self.__timber.log('GlacialTriviaQuestionRepository', f'Received an invalid trivia question type when fetching a question answer trivia question ({triviaType=}) ({fetchOptions=}) ({row=}): {exception}', exception, traceback.format_exc())
                raise exception

    async def __fetchMultipleChoiceOrTrueFalseTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions,
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
        originalTriviaSource = await self.__triviaSourceParser.parse(row[2])
        question = await self.__triviaQuestionCompiler.compileQuestion(row[3])
        triviaDifficulty = TriviaDifficulty.fromStr(row[4])
        triviaId: str = row[5]
        triviaType = TriviaQuestionType.fromStr(row[6])

        originalCorrectAnswers = await self.__fetchTriviaQuestionCorrectAnswers(
            connection = connection,
            triviaId = triviaId,
            triviaType = triviaType,
            originalTriviaSource = originalTriviaSource,
        )

        match triviaType:
            case TriviaQuestionType.MULTIPLE_CHOICE:
                multipleChoiceResponses = await self.__fetchTriviaQuestionMultipleChoiceResponses(
                    connection = connection,
                    triviaId = triviaId,
                    originalTriviaSource = originalTriviaSource,
                )

                await connection.close()

                return MultipleChoiceTriviaQuestion(
                    correctAnswers = originalCorrectAnswers,
                    multipleChoiceResponses = multipleChoiceResponses,
                    category = category,
                    categoryId = categoryId,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = originalTriviaSource,
                    triviaSource = self.triviaSource,
                )

            case TriviaQuestionType.TRUE_FALSE:
                await connection.close()

                return TrueFalseTriviaQuestion(
                    correctAnswer = utils.strictStrToBool(originalCorrectAnswers[0]),
                    category = category,
                    categoryId = categoryId,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = originalTriviaSource,
                    triviaSource = self.triviaSource,
                )

            case _:
                await connection.close()
                exception = UnsupportedTriviaTypeException(f'Received an invalid trivia question type! ({triviaType=}) ({fetchOptions=}) ({row=})')
                self.__timber.log('GlacialTriviaQuestionRepository', f'Received an invalid trivia question type when fetching a multiple choice or true false trivia question ({triviaType=}) ({fetchOptions=}) ({row=}): {exception}', exception, traceback.format_exc())
                raise exception

    async def __fetchQuestionAnswerTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions,
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
        originalTriviaSource = await self.__triviaSourceParser.parse(row[2])
        question = await self.__triviaQuestionCompiler.compileQuestion(row[3])
        triviaDifficulty = TriviaDifficulty.fromStr(row[4])
        triviaId: str = row[5]

        originalCorrectAnswers = await self.__fetchTriviaQuestionCorrectAnswers(
            connection = connection,
            triviaId = triviaId,
            triviaType = TriviaQuestionType.QUESTION_ANSWER,
            originalTriviaSource = originalTriviaSource,
        )

        await connection.close()

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(originalCorrectAnswers)
        compiledCorrectAnswers = await self.__buildCompiledCorrectAnswersForQuestionAnswerTrivia(originalCorrectAnswers)

        return QuestionAnswerTriviaQuestion(
            allWords = None,
            compiledCorrectAnswers = compiledCorrectAnswers,
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = triviaDifficulty,
            originalTriviaSource = originalTriviaSource,
            triviaSource = self.triviaSource,
        )

    async def fetchAllQuestionAnswerTriviaQuestions(
        self,
        fetchOptions: TriviaFetchOptions,
    ) -> FrozenList[QuestionAnswerTriviaQuestion]:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        if not await self.__triviaDatabaseFileExists():
            raise FileNotFoundError(f'Glacial trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        questions = await self.__fetchAllQuestionAnswerTriviaQuestions(fetchOptions)

        if questions is None or len(questions) == 0:
            raise NoTriviaQuestionException(f'Unable to fetch trivia questions from {self.triviaSource} ({fetchOptions=}) ({questions=})')

        return questions

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
            raise NoTriviaQuestionException(f'Unable to fetch trivia question from {self.triviaSource} ({fetchOptions=}) ({question=})')

        return question

    async def __fetchTriviaQuestionCorrectAnswers(
        self,
        connection: Connection,
        triviaId: str,
        triviaType: TriviaQuestionType,
        originalTriviaSource: TriviaSource,
    ) -> list[str]:
        cursor = await connection.execute(
            '''
                SELECT answer FROM glacialAnswers
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, ),
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
            triviaQuestionType = triviaType,
            triviaSource = originalTriviaSource,
        ):
            self.__timber.log('GlacialTriviaQuestionRepository', f'Added additional answers to question ({triviaId=})')

        return correctAnswers

    async def __fetchTriviaQuestionMultipleChoiceResponses(
        self,
        connection: Connection,
        triviaId: str,
        originalTriviaSource: TriviaSource,
    ) -> list[str]:
        cursor = await connection.execute(
            '''
                SELECT response FROM glacialResponses
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, ),
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
                questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED,
            ))

            questionAnswer = await self.__fetchQuestionAnswerTriviaQuestion(TriviaFetchOptions(
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId,
                questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED,
            ))

            hasQuestionSetAvailable = multipleChoiceOrTrueFalse is not None and questionAnswer is not None

        self.__hasQuestionSetAvailable = hasQuestionSetAvailable
        return hasQuestionSetAvailable

    async def remove(
        self,
        triviaId: str,
        originalTriviaSource: TriviaSource,
    ):
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
            (originalTriviaSource.toStr(), triviaId, ),
        )
        await cursor.close()

        cursor = await connection.execute(
            '''
                DELETE FROM glacialQuestions
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, ),
        )
        await cursor.close()

        cursor = await connection.execute(
            '''
                DELETE FROM glacialResponses
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            (originalTriviaSource.toStr(), triviaId, ),
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
        elif question.triviaSource is TriviaSource.GLACIAL:
            return False

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        await self.__createTablesIfNotExists(connection)

        if await self.__checkIfQuestionIsAlreadyStored(
            question = question,
            connection = connection,
        ):
            await connection.close()
            self.__timber.log('GlacialTriviaQuestionRepository', f'The given question already exists in the glacial trivia question database ({question=})')
            return False

        await self.__storeBaseTriviaQuestionData(
            question = question,
            connection = connection,
        )

        if question.triviaType is TriviaQuestionType.MULTIPLE_CHOICE and isinstance(question, MultipleChoiceTriviaQuestion):
            await self.__storeMultipleChoiceTriviaQuestion(
                connection = connection,
                question = question,
            )
        elif question.triviaType is TriviaQuestionType.QUESTION_ANSWER and isinstance(question, QuestionAnswerTriviaQuestion):
            await self.__storeQuestionAnswerTriviaQuestion(
                connection = connection,
                question = question,
            )
        elif question.triviaType is TriviaQuestionType.TRUE_FALSE and isinstance(question, TrueFalseTriviaQuestion):
            await self.__storeTrueFalseTriviaQuestion(
                connection = connection,
                question = question,
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
        connection: Connection,
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
            (question.category, question.categoryId, question.triviaSource.toStr(), question.question, question.triviaDifficulty.toStr(), question.triviaId, question.triviaType.toStr(), ),
        )

    async def __storeMultipleChoiceTriviaQuestion(
        self,
        connection: Connection,
        question: MultipleChoiceTriviaQuestion,
    ):
        if not isinstance(connection, Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')
        elif not isinstance(question, MultipleChoiceTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif question.triviaType is not TriviaQuestionType.MULTIPLE_CHOICE:
            raise ValueError(f'question class and TriviaQuestionType do not match ({question=}) ({question.triviaType=})')

        for correctAnswer in question.correctAnswers:
            await connection.execute_insert(
                '''
                    INSERT INTO glacialAnswers (answer, originalTriviaSource, triviaId)
                    VALUES ($1, $2, $3)
                ''',
                (correctAnswer, question.triviaSource.toStr(), question.triviaId, ),
            )

        for response in question.responses:
            await connection.execute_insert(
                '''
                    INSERT INTO glacialResponses (response, originalTriviaSource, triviaId)
                    VALUES ($1, $2, $3)
                ''',
                (response, question.triviaSource.toStr(), question.triviaId, ),
            )

    async def __storeQuestionAnswerTriviaQuestion(
        self,
        connection: Connection,
        question: QuestionAnswerTriviaQuestion,
    ):
        if not isinstance(connection, Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')
        elif not isinstance(question, QuestionAnswerTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif question.triviaType is not TriviaQuestionType.QUESTION_ANSWER:
            raise ValueError(f'question class and TriviaQuestionType do not match ({question=}) ({question.triviaType=})')

        for answer in question.originalCorrectAnswers:
            await connection.execute_insert(
                '''
                    INSERT INTO glacialAnswers (answer, originalTriviaSource, triviaId)
                    VALUES ($1, $2, $3)
                ''',
                (answer, question.triviaSource.toStr(), question.triviaId, ),
            )

    async def __storeTrueFalseTriviaQuestion(
        self,
        connection: Connection,
        question: TrueFalseTriviaQuestion,
    ):
        if not isinstance(connection, Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')
        elif not isinstance(question, TrueFalseTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif question.triviaType is not TriviaQuestionType.TRUE_FALSE:
            raise ValueError(f'question class and TriviaQuestionType do not match ({question=}) ({question.triviaType=})')

        correctAnswer = str(question.correctAnswer).lower()

        await connection.execute_insert(
            '''
                INSERT INTO glacialAnswers (answer, originalTriviaSource, triviaId)
                VALUES ($1, $2, $3)
            ''',
            (correctAnswer, question.triviaSource.toStr(), question.triviaId, ),
        )

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return {
            TriviaQuestionType.MULTIPLE_CHOICE,
            TriviaQuestionType.QUESTION_ANSWER,
            TriviaQuestionType.TRUE_FALSE,
        }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.GLACIAL
