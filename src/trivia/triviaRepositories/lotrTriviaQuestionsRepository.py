from typing import Any

import aiofiles
import aiofiles.ospath
import aiosqlite
from ...timber.timberInterface import TimberInterface
from ..additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from ..compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface
from ..compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaFetchOptions import TriviaFetchOptions
from .absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from ..triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from ...misc import utils as utils


class LotrTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'lotrTriviaQuestionsDatabase.sqlite'
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
        elif not utils.isValidStr(triviaDatabaseFile):
            raise TypeError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__hasQuestionSetAvailable: bool | None = None

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('LotrTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('LotrTriviaQuestionRepository', f'{triviaDict}')

        question = utils.getStrFromDict(triviaDict, 'question')
        question = await self.__triviaQuestionCompiler.compileQuestion(question)

        triviaId = utils.getStrFromDict(triviaDict, 'triviaId')

        originalCorrectAnswers: list[str] = list()
        originalCorrectAnswers.extend(triviaDict['correctAnswers'])

        correctAnswers: list[str] = list()
        correctAnswers.extend(originalCorrectAnswers)

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = correctAnswers,
            triviaId = triviaId,
            triviaQuestionType = TriviaQuestionType.QUESTION_ANSWER,
            triviaSource = self.getTriviaSource()
        ):
            self.__timber.log('LotrTriviaQuestionRepository', f'Added additional answers to question ({triviaId=})')

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(correctAnswers)

        cleanedCorrectAnswers: list[str] = list()
        cleanedCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(correctAnswers)

        expandedCorrectAnswers: set[str] = set()
        for answer in cleanedCorrectAnswers:
            expandedCorrectAnswers.update(await self.__triviaAnswerCompiler.expandNumerals(answer))

        return QuestionAnswerTriviaQuestion(
            correctAnswers = correctAnswers,
            cleanedCorrectAnswers = list(expandedCorrectAnswers),
            category = 'Lord of the Rings',
            categoryId = None,
            originalCorrectAnswers = originalCorrectAnswers,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = self.getTriviaSource()
        )

    async def __fetchTriviaQuestionDict(self) -> dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'LOTR trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT answerA, answerB, answerC, answerD, question, triviaId FROM lotrQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        if not utils.hasItems(row) or len(row) != 6:
            raise RuntimeError(f'Received malformed data from LOTR database: {row}')

        correctAnswers: list[str] = list()
        self.__selectiveAppend(correctAnswers, row[0])
        self.__selectiveAppend(correctAnswers, row[1])
        self.__selectiveAppend(correctAnswers, row[2])
        self.__selectiveAppend(correctAnswers, row[3])

        if not utils.hasItems(correctAnswers):
            raise RuntimeError(f'Received malformed correct answer data from LOTR database: {row}')

        triviaQuestionDict: dict[str, Any] = {
            'correctAnswers': correctAnswers,
            'question': row[4],
            'triviaId': row[5]
        }

        await cursor.close()
        await connection.close()
        return triviaQuestionDict

    def getSupportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.QUESTION_ANSWER }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.LORD_OF_THE_RINGS

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable

    def __selectiveAppend(self, correctAnswers: list[str], correctAnswer: str | None):
        if not isinstance(correctAnswers, list):
            raise TypeError(f'correctAnswers argument is malformed: \"{correctAnswers}\"')

        if utils.isValidStr(correctAnswer):
            correctAnswers.append(correctAnswer)
