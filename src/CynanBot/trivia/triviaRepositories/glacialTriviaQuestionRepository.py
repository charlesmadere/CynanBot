import traceback
from typing import List, Set

import aiofiles
import aiofiles.ospath
import aiosqlite
from aiosqlite import Connection

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
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


class GlacialTriviaQuestionRepository(
    AbsTriviaQuestionRepository,
    GlacialTriviaQuestionRepositoryInterface
):

    def __init__(
        self,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        triviaDatabaseFile: str = 'glacialTriviaQuestionsDatabase.sqlite'
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not utils.isValidStr(triviaDatabaseFile):
            raise TypeError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__areTablesCreated: bool = False
        self.__hasQuestionSetAvailable: bool | None = None

    async def __checkIfQuestionIsAlreadyStored(
        self,
        question: AbsTriviaQuestion,
        connection: Connection
    ):
        cursor = await connection.execute(
            '''
                SELECT EXISTS(
                    SELECT 1 FROM glacialQuestions
                    WHERE originalTriviaSource = $1 AND triviaId = $2
                    LIMIT 1
                )
            ''',
            question.getTriviaSource().toStr(), question.getTriviaId()
        )

        row = await cursor.fetchone()
        await cursor.close()

        return row is not None and len(row) >= 1

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

    async def __fetchAnyTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions
    ) -> AbsTriviaQuestion | None:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT answerA, answerB, answerC, answerD, answerE, answerF, correctAnswer, question, triviaDifficulty, triviaId, triviaType FROM glacialQuestions
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

        # TODO

        await connection.close()

        raise RuntimeError('not implemented')

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
            TriviaQuestionType.MULTIPLE_CHOICE.toStr(), TriviaQuestionType.TRUE_FALSE.toStr()
        )

        row = await cursor.fetchone()
        await cursor.close()

        if row is None or len(row) == 0:
            await connection.close()
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any {TriviaQuestionType.MULTIPLE_CHOICE} or {TriviaQuestionType.TRUE_FALSE} question in the database! ({fetchOptions=})')
            return None

        category: str | None = row[0]
        categoryId: str | None = row[1]
        originalTriviaSource = TriviaSource.fromStr(row[2])
        question: str = row[3]
        triviaDifficulty = TriviaDifficulty.fromStr(row[4])
        triviaId: str = row[5]
        triviaType = TriviaQuestionType.fromStr(row[6])

        answers = await self.__fetchTriviaQuestionAnswers(
            connection = connection,
            triviaId = triviaId,
            originalTriviaSource = originalTriviaSource
        )

        responses = await self.__fetchTriviaQuestionResponses(
            connection = connection,
            triviaId = triviaId,
            originalTriviaSource = originalTriviaSource
        )

        await connection.close()

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            return MultipleChoiceTriviaQuestion(
                correctAnswers = answers,
                multipleChoiceResponses = responses,
                category = category,
                categoryId = categoryId,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                triviaSource = self.getTriviaSource()
            )
        elif triviaType is TriviaQuestionType.TRUE_FALSE:
            return TrueFalseTriviaQuestion(
                correctAnswers = answers,
                category = category,
                categoryId = categoryId,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                triviaSource = self.getTriviaSource()
            )
        else:
            exception = UnsupportedTriviaTypeException(f'Received an invalid trivia question type! ({triviaType=}) ({fetchOptions=}) ({row=})')
            self.__timber.log('GlacialTriviaQuestionRepository', f'Received an invalid trivia question type when fetching a trivia question ({triviaType=}) ({fetchOptions=}) ({row=}): {exception}', exception, traceback.format_exc())
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
            TriviaQuestionType.QUESTION_ANSWER.toStr()
        )

        row = await cursor.fetchone()
        await cursor.close()

        if row is None or len(row) == 0:
            await connection.close()
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any {TriviaQuestionType.QUESTION_ANSWER} question in the database! ({fetchOptions=})')
            return None

        category: str | None = row[0]
        categoryId: str | None = row[1]
        originalTriviaSource = TriviaSource.fromStr(row[2])
        question: str = row[3]
        triviaDifficulty = TriviaDifficulty.fromStr(row[4])
        triviaId: str = row[5]

        answers = await self.__fetchTriviaQuestionAnswers(
            connection = connection,
            triviaId = triviaId,
            originalTriviaSource = originalTriviaSource
        )

        await connection.close()

        return QuestionAnswerTriviaQuestion(
            correctAnswers = answers,
            cleanedCorrectAnswers = answers,
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = triviaDifficulty,
            triviaSource = self.getTriviaSource()
        )

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
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

    async def __fetchTriviaQuestionAnswers(
        self,
        connection: Connection,
        triviaId: str,
        originalTriviaSource: TriviaSource
    ) -> List[str]:
        cursor = await connection.execute(
            '''
                SELECT answer FROM glacialAnswers
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            originalTriviaSource.toStr(), triviaId
        )

        rows = await cursor.fetchall()
        await cursor.close()

        if rows is None or len(rows) == 0:
            exception = NoTriviaCorrectAnswersException(f'No trivia answers found! ({triviaId=}) ({originalTriviaSource=})')
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any trivia answers for {triviaId=} and {originalTriviaSource=}: {exception}', exception, traceback.format_exc())
            raise exception

        responses: Set[str] = set()

        for row in rows:
            responses.add(row[0])

        return list(responses)

    async def __fetchTriviaQuestionResponses(
        self,
        connection: Connection,
        triviaId: str,
        originalTriviaSource: TriviaSource
    ) -> List[str]:
        cursor = await connection.execute(
            '''
                SELECT response FROM glacialResponses
                WHERE originalTriviaSource = $1 AND triviaId = $2
            ''',
            originalTriviaSource.toStr(), triviaId
        )

        rows = await cursor.fetchall()
        await cursor.close()

        if rows is None or len(rows) == 0:
            exception = NoTriviaMultipleChoiceResponsesException(f'No trivia responses found! ({triviaId=}) ({originalTriviaSource=})')
            self.__timber.log('GlacialTriviaQuestionRepository', f'Unable to find any trivia responses for {triviaId=} and {originalTriviaSource=}: {exception}', exception, traceback.format_exc())
            raise exception

        responses: Set[str] = set()

        for row in rows:
            responses.add(row[0])

        return list(responses)

    async def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return {
            TriviaQuestionType.MULTIPLE_CHOICE,
            TriviaQuestionType.QUESTION_ANSWER,
            TriviaQuestionType.TRUE_FALSE
        }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.GLACIAL

    async def hasQuestionSetAvailable(self) -> bool:
        hasQuestionSetAvailable = self.__hasQuestionSetAvailable

        if hasQuestionSetAvailable is None:
            hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)

            if hasQuestionSetAvailable:
                twitchChannel = await self.__twitchHandleProvider.getTwitchHandle()

                multipleChoiceOrTrueFalse = await self.__fetchMultipleChoiceOrTrueFalseTriviaQuestion(TriviaFetchOptions(
                    twitchChannel = twitchChannel,
                    questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
                ))

                questionAnswer = await self.__fetchQuestionAnswerTriviaQuestion(TriviaFetchOptions(
                    twitchChannel = twitchChannel,
                    questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
                ))

                hasQuestionSetAvailable = multipleChoiceOrTrueFalse is not None and questionAnswer is not None

            self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable

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
            raise BadTriviaTypeException(f'The given question is a confusing/malformed/misconstrued trivia type ({question=})')

        await connection.close()
        self.__timber.log('GlacialTriviaQuestionRepository', f'Added a new question into the glacial trivia question database ({question=})')
        return True

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

        pass

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

        # TODO
        pass

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

        await connection.execute(
            '''
                INSERT INTO glacialQuestions (category, categoryId, originalTriviaSource, question, triviaDifficulty, triviaId, triviaType)
                VALUES ($1, $2)
            ''',
            question.getCategory(), question.getCategoryId(), question.getTriviaSource().toStr(), question.getQuestion(), question.getTriviaDifficulty().toStr(), question.getTriviaId(), TriviaQuestionType.TRUE_FALSE.toStr()
        )

        for answer in question.getCorrectAnswerBools():
            # TODO write bools to glacialAnswers
            pass
